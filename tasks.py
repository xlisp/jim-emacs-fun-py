import asyncio


async def my_coroutine():
    print('Coroutine started')
    await asyncio.sleep(1)
    print('Coroutine finished')


async def main():
    task = asyncio.create_task(my_coroutine())
    await task


asyncio.run(main())
