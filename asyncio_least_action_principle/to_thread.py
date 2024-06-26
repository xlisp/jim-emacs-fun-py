import asyncio
import time

## 在不同的线程中异步地运行函数 func。
## 这个协程函数主要是用于执行在其他情况下会阻塞事件循环的 IO 密集型函数/方法。 例如:
def blocking_io():
    print(f"start blocking_io at {time.strftime('%X')}")
    # Note that time.sleep() can be replaced with any blocking
    # IO-bound operation, such as file operations.
    time.sleep(1)
    print(f"blocking_io complete at {time.strftime('%X')}")

async def main():
    print(f"started main at {time.strftime('%X')}")

    await asyncio.gather(
        asyncio.to_thread(blocking_io),
        asyncio.sleep(1))

    print(f"finished main at {time.strftime('%X')}")


asyncio.run(main())

# started main at 23:14:53
# start blocking_io at 23:14:53
# blocking_io complete at 23:14:54
# finished main at 23:14:54
#
