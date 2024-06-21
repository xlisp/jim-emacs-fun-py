import asyncio

async def my_coroutine():
    print('Coroutine started')
    await asyncio.sleep(1)
    print('Coroutine finished')

loop = asyncio.get_event_loop()
loop.run_until_complete(my_coroutine())
loop.close()

# Coroutine started
# Coroutine finished

