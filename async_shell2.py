import asyncio
from asyncio.subprocess import Process, PIPE
from asyncio.streams import StreamReader

async def main():
    process: Process = await asyncio.create_subprocess_exec(
        "ls", "-la", stdout=PIPE)
    print(f"进程的 pid: {process.pid}")
    await process.wait()
    # 当子进程执行完毕时，拿到它的 stdout 属性
    stdout: StreamReader = process.stdout
    # 读取输出内容，如果子进程没有执行完毕，那么 await stdout.read() 会阻塞
    content = (await stdout.read()).decode("utf-8")
    print(content) #print(content[: 100])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
