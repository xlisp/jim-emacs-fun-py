import asyncio
async def long_running_task():
    print("long_running_task====")
    await asyncio.sleep(10)

# 备注 asyncio.timeout() 上下文管理器负责将 asyncio.CancelledError 转化为 TimeoutError，这意味着 TimeoutError 只能在该上下文管理器 之外 被捕获。
async def main():
    try:
        async with asyncio.timeout(3): # 超时的处理，这个很有用！！！
            await long_running_task()
    except TimeoutError:
        print("The long operation timed out, but we've handled it.")

    print("This statement will run regardless.")

asyncio.run(main())
# long_running_task====
# The long operation timed out, but we've handled it.
# This statement will run regardless.
#
