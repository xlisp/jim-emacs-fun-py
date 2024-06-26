import asyncio

# 一个创建然后并发地运行任务等待它们完成的新选择是 asyncio.TaskGroup。 TaskGroup 提供了针对调度嵌套子任务的比 gather 更强的安全保证：如果一个任务（或子任务，即由一个任务调度的任务）引发了异常，TaskGroup 将取消剩余的已排期任务）。
async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    return f

async def main():
    # Schedule three calls *concurrently*:
    L = await asyncio.gather( # 并发运行任务
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )
    print(L)

asyncio.run(main())
# Task A: Compute factorial(2), currently i=2...
# Task B: Compute factorial(3), currently i=2...
# Task C: Compute factorial(4), currently i=2...
# Task A: factorial(2) = 2
# Task B: Compute factorial(3), currently i=3...
# Task C: Compute factorial(4), currently i=3...
# Task B: factorial(3) = 6
# Task C: Compute factorial(4), currently i=4...
# Task C: factorial(4) = 24
# [2, 6, 24]
#
