import time
import asyncio

# 定义异步函数
async def hello():
    await asyncio.sleep(1)
    print('Hello World:%s' % time.time())

# 获取事件循环: 事件循环EventLoop.jpg
loop = asyncio.get_event_loop()

loop.run_until_complete(hello()) #=> Hello World:1719411143.132673
