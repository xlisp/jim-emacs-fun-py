
import time
import asyncio


async def fun():
    time.sleep(3)  # 第一台洗衣机,
    print('washer1 finished')  # 洗完了


coroutine_1 = fun()  # 协程是一个对象，不能直接运行
loop = asyncio.get_event_loop()  # 创建一个事件循环
result = loop.run_until_complete(coroutine_1)  # 将协程对象加入到事件循环中，并执行

print(result) #=> 
## washer1 finished
## None
