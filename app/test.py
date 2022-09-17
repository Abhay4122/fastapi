import asyncio, datetime, time

# async def hello():
#     print(f'Hello...')
#     # await foo()
#     task = asyncio.create_task(foo())
#     # await task
#     await asyncio.sleep(1)
#     print(f'...World!')

# async def foo():
#     print('Pritty')
#     await asyncio.sleep(4)



# asyncio.run(hello())



#*******************************************************************************

async def fetch_data():
    print('Fetching start')
    await asyncio.sleep(2)
    print('Fetching Done')
    return {'data': 1}

async def print_numbers():
    for i in range(10):
        print(i)
        await asyncio.sleep(0.25)
    
    return 'task2 run successfully'

async def main():
    task1 = asyncio.create_task(fetch_data())
    task2 = asyncio.create_task(print_numbers())

    # a = await asyncio.gather(*[task2, task1])

    # print(a)

    # await task2
    # await task1
    # print(value) 

# asyncio.run(main())
def run():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
        loop.run_forever()
        # loop.close()
    finally:
        tasks = [task.cancel() for task in asyncio.all_tasks()
        if task is not asyncio.current_task()]
        loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()

run()




    
