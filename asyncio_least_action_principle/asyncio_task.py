
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")

# asyncio.run() 函数用来运行最高层级的入口点 "main()" 函数 (参见上面的示例。) => 一个项目只有一个asyncio.run()！ =》全部都不阻塞的工作！才能扛住几万连接和并发
asyncio.run(main())
# started at 22:31:50
# hello
# world
# finished at 22:31:53
#
