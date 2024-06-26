import time
import asyncio


async def washing1():
    time.sleep(3)  # 第一台洗衣机,
    print('washer1 finished')  # 洗完了


async def washing2():
    time.sleep(8)
    print('washer2 finished')


async def washing3():
    time.sleep(5)
    print('washer3 finished')


async def main():
    print('start main:')
    start_time = time.time()
    task1 = asyncio.create_task(washing1())
    task2 = asyncio.create_task(washing2())
    task3 = asyncio.create_task(washing3())
    await task1
    await task2
    await task3
    end_time = time.time()
    print('-----------end main----------')
    print('总共耗时:{}'.format(end_time-start_time))


if __name__ == '__main__':
    # asyncio.run(main())
    loop = asyncio.get_event_loop()  # 创建一个事件循环
    result = loop.run_until_complete(main())  # 将协程对象加入到事件循环中，并执行

# => 
# start main:
# washer1 finished
# washer2 finished
# washer3 finished
# -----------end main----------
# 总共耗时:16.015585899353027
# 
