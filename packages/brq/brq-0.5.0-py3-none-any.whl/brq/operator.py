from datetime import datetime
from typing import Any, AsyncIterator

import redis.asyncio as redis

from brq.log import logger
from brq.models import Job
from brq.rds import RedisOperator


class BrqOperator(RedisOperator):
    def __init__(
        self,
        redis: redis.Redis | redis.RedisCluster,
        redis_prefix: str = "brq",
        redis_seperator: str = ":",
    ):
        super().__init__(redis_prefix, redis_seperator)
        self.redis = redis

    async def enque_deferred_job(self, function_name: str, maxlen: int = 1000):
        """
        From zset to stream
        """
        lua_script = """
        local zset_key = KEYS[1]
        local stream_key = KEYS[2]
        local current_timestamp = ARGV[1]
        local maxlen = ARGV[2]

        local elements = redis.call('ZRANGEBYSCORE', zset_key, '-inf', current_timestamp)

        for i, element in ipairs(elements) do
            redis.call('ZREM', zset_key, element)
            redis.call('XADD', stream_key, 'MAXLEN', maxlen, '*', 'payload', element)
        end
        return #elements
        """
        defer_key = self.get_deferred_key(function_name)
        stream_name = self.get_stream_name(function_name)

        elements = await self.redis.eval(
            lua_script,
            2,
            defer_key,
            stream_name,
            await self.get_current_timestamp_ms(self.redis),
            maxlen,
        )
        if elements:
            logger.debug(f"Enqueued {elements} deferred jobs")

    async def _remove_deferred_job(
        self,
        function_name: str,
        job: Job,
    ):
        """
        Remove specific deferred job

        Args:
            function_name (str): function name
            job (Job): job to be removed
        """
        defer_key = self.get_deferred_key(function_name)
        delete_nums = await self.redis.zrem(defer_key, job.to_redis())
        logger.info(f"Removed {delete_nums} deferred jobs")

    async def get_defer_timestamp_ms(
        self,
        defer_until: datetime | None = None,
        defer_hours: int = 0,
        defer_minutes: int = 0,
        defer_seconds: int = 0,
    ) -> int | None:
        if not any(
            [
                defer_until,
                defer_hours,
                defer_minutes,
                defer_seconds,
            ]
        ):
            return None

        if defer_until:
            logger.debug(f"Using defer_until, ignore defer_hours, defer_minutes, defer_seconds")
            defer_until = defer_until.timestamp()

        else:
            defer_until = (
                await self.get_current_timestamp(self.redis)
                + defer_hours * 60 * 60
                + defer_minutes * 60
                + defer_seconds
            )

        return defer_until * 1000

    async def get_deferred_jobs(
        self,
        function_name: str,
        start_timestamp: str | int = "-inf",
        end_timestamp: str | int = "+inf",
    ) -> dict[datetime:Job]:
        """
        Get all deferred jobs

        Args:
            function_name (str): function name
            start_timestamp (str | int, optional): start timestamp in millisecond. Defaults to "-inf".
            end_timestamp (str | int, optional): end timestamp in millisecond. Defaults to "+inf".

        Returns:
            dict[datetime:Job]: deferred jobs,
                key is the datetime when the job expected to be executed
                value is the job
        """
        defer_key = self.get_deferred_key(function_name)
        return {
            datetime.fromtimestamp(float(element[1]) / 1000): Job.from_redis(element[0])
            for element in await self.redis.zrangebyscore(
                defer_key, start_timestamp, end_timestamp, withscores=True
            )
        }

    async def get_dead_messages(self, function_name: str) -> dict[datetime:Job]:
        """
        Get all dead messages

        Args:
            function_name (str): function name

        Returns:
            dict[datetime:Job]: dead messages,
                key is the datetime when the job to be moved to dead message
                value is the job
        """
        dead_key = self.get_dead_message_key(function_name)
        return {
            datetime.fromtimestamp(float(element[1]) / 1000): Job.from_redis(element[0])
            for element in await self.redis.zrangebyscore(dead_key, "-inf", "+inf", withscores=True)
        }

    async def count_deferred_jobs(self, function_name: str) -> int:
        defer_key = self.get_deferred_key(function_name)
        if not await self.redis.exists(defer_key):
            return 0
        return await self.redis.zcard(defer_key)

    async def count_stream(self, function_name: str) -> int:
        """
        Count stream length

        If Consumer's `delete_message_after_process` if False, will include already processed messages
        """
        stream_name = self.get_stream_name(function_name)
        if not await self.redis.exists(stream_name):
            return 0
        return await self.redis.xlen(stream_name)

    async def count_stream_added(self, function_name: str) -> int:
        stream_name = self.get_stream_name(function_name)
        if not await self.redis.exists(stream_name):
            return 0

        xinfo_stream = await self.redis.xinfo_stream(stream_name)
        return xinfo_stream.get("entries-added")

    async def count_processing_jobs(
        self, function_name: str, group_name: str = "default-workers"
    ) -> int:
        return await self.count_unacked_jobs(function_name, group_name)

    async def count_unacked_jobs(
        self, function_name: str, group_name: str = "default-workers"
    ) -> int:
        """
        Count unacked jobs in group

        Args:
            function_name (str): function name
            group_name (str, optional): group name. Defaults to "default-workers". Should be the same as Consumer's `group_name`
        """
        stream_name = self.get_stream_name(function_name)
        if not await self.redis.exists(stream_name):
            return 0
        try:
            consumer_group_info = await self.redis.xinfo_consumers(stream_name, group_name)
            return consumer_group_info[0]["pending"] if consumer_group_info else 0
        except redis.ResponseError as e:
            if "NOGROUP No such consumer group" in e.args[0]:
                return 0
            raise

    async def count_undelivered_jobs(
        self, function_name: str, group_name: str = "default-workers"
    ) -> int | None:
        """
        Only available when redis >= 7.0, None if can't be determined.
        """
        stream_name = self.get_stream_name(function_name)
        if not await self.redis.exists(stream_name):
            return 0

        gropu_infos = await self.redis.xinfo_groups(stream_name)
        for group_info in gropu_infos:
            if group_info["name"] == group_name:
                return group_info.get("lag", None)
        return await self.count_stream(function_name)

    async def count_unprocessed_jobs(
        self, function_name: str, group_name: str = "default-workers"
    ) -> int:
        """
        If redis >= 7.0, it will be the sum of `count_undelivered_jobs` and `count_unacked_jobs`
        Otherwise, it only includes `count_unacked_jobs`
        """
        stream_name = self.get_stream_name(function_name)
        if not await self.redis.exists(stream_name):
            return 0

        gropu_infos = await self.redis.xinfo_groups(stream_name)
        for group_info in gropu_infos:
            if group_info["name"] == group_name:
                pending = group_info.get("pending") or 0
                lag = group_info.get("lag")
                if lag is None:
                    logger.warning(
                        f"Lag is not available for group `{group_name}` in stream `{stream_name}`. Try calculate it."
                    )
                    """
                    1. Is empty
                    2. Stream last-generated-id were deleted, the lag possibly is length of stream
                    """
                    entries_read = group_info.get("entries-read")
                    if entries_read is None:
                        return pending
                    added_count = await self.count_stream_added(function_name)
                    if added_count is None:
                        return pending
                    return added_count - entries_read - pending
                return lag + pending
        return await self.count_stream(function_name)

    async def count_dead_messages(self, function_name: str) -> int:
        dead_key = self.get_dead_message_key(function_name)
        if not await self.redis.exists(dead_key):
            return 0
        return await self.redis.zcard(dead_key)

    async def remove_dead_message(self, function_name: str, job: Job):
        dead_key = self.get_dead_message_key(function_name)
        await self.redis.zrem(dead_key, job.to_redis())

    async def emit_deferred_job(self, function_name: str, defer_until: int, job: Job):
        defer_key = self.get_deferred_key(function_name)
        await self.redis.zadd(defer_key, {job.to_redis(): defer_until})
        return job

    async def _deferred_job_exists(
        self,
        function_name: str,
        job: Job,
    ) -> bool:
        defer_key = self.get_deferred_key(function_name)
        return await self.redis.zscore(defer_key, job.to_redis())

    async def walk_jobs(self, function_name: str, count=None) -> AsyncIterator[Job]:
        message_id = "0-0"
        while True:
            messages = await self.redis.xread(
                {self.get_stream_name(function_name): message_id}, count=count
            )
            if not messages or not messages[0]:
                break

            messages = messages[0][1]
            for message_id, body in messages:
                yield Job.from_redis(body["payload"])
