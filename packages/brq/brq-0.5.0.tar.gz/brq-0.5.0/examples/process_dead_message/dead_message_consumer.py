import os

from brq.consumer import Consumer
from brq.daemon import Daemon
from brq.tools import get_redis_client, get_redis_url


async def echo(message):
    print(message)


async def main():
    redis_url = get_redis_url(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=int(os.getenv("REDIS_DB", 0)),
        cluster=bool(os.getenv("REDIS_CLUSTER", False)),
        tls=bool(os.getenv("REDIS_TLS", False)),
    )
    async with get_redis_client(redis_url) as async_redis_client:
        await Consumer(async_redis_client, echo).process_dead_jobs()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
