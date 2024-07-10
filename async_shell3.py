import asyncio
from asyncio.subprocess import Process, PIPE
from asyncio.streams import StreamReader

#"sgpt", "--no-interaction", "--shell",
async def main(question):
    process: Process = await asyncio.create_subprocess_exec(
        #'sgpt --shell "install npm lib" --no-interaction',
        "sgpt", "--no-interaction", "--shell",
        question, stdout=PIPE)
    print(f"进程的 pid: {process.pid}")
    await process.wait()
    # 当子进程执行完毕时，拿到它的 stdout 属性
    stdout: StreamReader = process.stdout
    # 读取输出内容，如果子进程没有执行完毕，那么 await stdout.read() 会阻塞
    content = (await stdout.read()).decode("utf-8")
    print(content) #print(content[: 100])


loop = asyncio.get_event_loop()
loop.run_until_complete(main("'install npm lib pm2 '"))

#=> npm install pm2 && echo 'pm2 installed'
