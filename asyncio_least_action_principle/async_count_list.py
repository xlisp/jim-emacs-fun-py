
import asyncio

async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")

# 在 async 函数main的里面，asyncio.gather() 方法将多个异步任务（三个 count()）包装成一个新的异步任务，必须等到内部的多个异步任务都执行结束，这个新的异步任务才会结束
async def main():
    await asyncio.gather(count(), count(), count())

asyncio.run(main())
# =>
# One
# One
# One
# Two
# Two
# Two
#
