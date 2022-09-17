import asyncio
import logging
import random
import signal
import time

LOG_FMT_STR = "%(asctime)s :: %(name)s ::: %(levelname)s :: %(message)s"
LOG_DATEFMT_STR = "%d-%b-%y %H:%M:%S"


logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FMT_STR,
    datefmt=LOG_DATEFMT_STR,
    handlers=[
        logging.FileHandler(
            filename="test-async.log",
            mode="w",
        ),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


async def consumer(name: str, queue: asyncio.Queue):
    while True:
        logger.info(f"{name}: {await queue.get()}")
        await asyncio.sleep(random.random())


async def publish(queue: asyncio.Queue, data=None):
    # for i in range(100):
    #     await asyncio.sleep(random.random())
    #     logger.info(f"Publish: {i}")
    #     asyncio.create_task(queue.put(i))
    #     # await queue.put(i)
    await asyncio.sleep(random.random())
    logger.info(f"Publish: {data}")
    await queue.put(f'Data: {data}')
    # asyncio.create_task(queue.put(f'Data: {data}'))


def publish_sync(queue: asyncio.Queue, data=None):
    # for i in range(100):
    #     await asyncio.sleep(random.random())
    #     logger.info(f"Publish: {i}")
    #     asyncio.create_task(queue.put(i))
    #     # await queue.put(i)
    time.sleep(random.random())
    logger.info(f"Publish: {data}")
    queue.put_nowait(f'Data: {data}')
    # asyncio.create_task(queue.put(f'Data: {data}'))


async def worker(name, queue):
    while True:
        # Get a "work item" out of the queue.
        sleep_for = await queue.get()

        # Sleep for the "sleep_for" seconds.
        await asyncio.sleep(sleep_for)

        # Notify the queue that the "work item" has been processed.
        queue.task_done()

        logger.info(f'{name} has slept for {sleep_for:.2f} seconds')


def callback_function(future: asyncio.Future):
    result = future.result()


async def engine(name, queue):
    while True:
        # Get a "work item" out of the queue.
        sleep_for = await queue.get()

        # Sleep for the "sleep_for" seconds.
        await asyncio.sleep(sleep_for)

        # Notify the queue that the "work item" has been processed.
        queue.task_done()

        logger.info(f'{name} has slept for {sleep_for:.2f} seconds')


async def workload(queue):
    # Create a queue that we will use to store our "workload".

    # Generate random timings and put them into the queue.
    total_sleep_time = 0
    for _ in range(20):
        sleep_for = random.uniform(0.05, 1.0)
        total_sleep_time += sleep_for
        queue.put_nowait(sleep_for)

    # Create three worker tasks to process the queue concurrently.
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    # Wait until the queue is fully processed.
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)

    logger.info('====')
    logger.info(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
    logger.info(f'total expected sleep time: {total_sleep_time:.2f} seconds')


# async def run(queue: asyncio.Queue, loop: asyncio.AbstractEventLoop):
#     delay_timestamp = {}
#     take_names = [f'dcu-{i}' for i in range(1)]
#     for i in range(100):
#         # await publish(queue, i)
#         task = random.choice(take_names)
#         try:
#             last_time = delay_timestamp[task]
#             # logger.info(f'{task} is already in queue')
#         except KeyError:
#             last_time = loop.time()
#             # logger.info(f'{task} is not in queue')
#             delay_timestamp[task] = last_time
#         current_time = loop.time()
#         delay_time = 3 - (current_time - last_time)
#         if delay_time < 0:
#             delay_time = 0
#         # logger.info(f'{task} last time: {last_time}')
#         # logger.info(f'{task} current time: {current_time}')
#         logger.info(f'Task {i} {task} delay time: {delay_time}')
#         # await asyncio.sleep(delay_time)
#         # asyncio.create_task(publish(queue, i))
#         loop.call_later(delay_time, loop.create_task, publish(queue, i))
#         delay_timestamp[task] = loop.time() + delay_time
#         # logger.info(delay_timestamp)
#         # delay_timestamp[task] = loop.time() + delay_time
#         # logger.info(delay_timestamp)

async def run(queue: asyncio.Queue):
    for i in range(100):
        # await publish(queue, i)
        asyncio.create_task(publish(queue, i))


async def shutdown(loop, signal):
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    logger.info(f'Cancelling {len(tasks)} tasks')
    logger.info(f'{len(tasks)} tasks')
    logger.info('foo-5' in [task.get_name() for task in tasks])
    for task in tasks:
        logger.info(task.get_name())
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


def main():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    queue = asyncio.Queue()
    task_queue = asyncio.Queue()
    worker_queue = asyncio.Queue()
    info_queue = asyncio.Queue()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT, signal.SIGABRT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown(loop, s))
        )
    try:
        # loop.run_until_complete(workload(queue))
        loop.create_task(run(queue))
        # loop.create_task(consumer(f'Consumer-{1}', queue))
        consumers_count = 100
        for i in range(consumers_count):
            # # loop.call_later(2, loop.create_task, consumer(f'Consumer-{i+1}', queue))
            # loop.run_until_complete(asyncio.sleep(2))
            loop.create_task(consumer(f'Consumer-{i+1}', queue))
        loop.run_forever()
    finally:
        # logger.info(asyncio.all_tasks())
        loop.close()


if __name__ == '__main__':
    main()
