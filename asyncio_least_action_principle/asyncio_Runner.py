import asyncio

async def main():
    await asyncio.sleep(1)
    print('hello')

# 跑整个事件流循环
with asyncio.Runner() as runner:
    runner.run(main())
