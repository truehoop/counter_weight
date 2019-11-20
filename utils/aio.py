import asyncio

# from sanic.log import logger

from utils.time import now_ms_ts


def count_all_async_tasks():
    return len(asyncio.Task.all_tasks())


async def loop_counter(interval=10):
    while True:
        # logger.info(f"Tasks count: {count_all_async_tasks()}")
        await asyncio.sleep(interval)


async def loop_ms_timestamp(interval=10):
    while True:
        now_ms = now_ms_ts()
        # logger.info(f'loop_ms_timestamp {now_ms}')
        await asyncio.sleep(interval)
