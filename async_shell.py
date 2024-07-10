# https://www.cnblogs.com/traditional/p/17399054.html
import asyncio
from asyncio.subprocess import Process

async def main():
    process: Process = await asyncio.create_subprocess_exec("ls", "-l")
    print(f"进程的 pid: {process.pid}")
    # 等待子进程执行完毕，并返回状态码
    status_code = await process.wait()
    print(f"status code: {status_code}")

asyncio.run(main())
