import asyncio
from asyncio import Queue

a = Queue()
b = Queue()

# a: <Queue at 0x13a730b10 maxsize=0 tasks=3>
# b: <Queue at 0x13aa1efd0 maxsize=0 tasks=1>

async def log_scribe():
    #a = Queue()  # Our channel A, the log's main door

    async def logging_loop():
        while True:
            msg = await a.get()
            if msg is None:
                break
            print("Logging:", msg)

    asyncio.create_task(logging_loop())
    return a

async def log_listener(a):
    # b = Queue()  # Channel B, to hear and see

    async def listener_loop():
        while True:
            msg = await b.get()
            if msg is None:
                break
            print("Listener:", msg)

    async def forward_logs():
        while True:
            msg = await a.get()
            if msg is None:
                await b.put(None)
                break
            await b.put(msg)

    asyncio.create_task(listener_loop())
    asyncio.create_task(forward_logs())
    return b

async def main():
    a = await log_scribe()  # Call the scribe to start the play
    b = await log_listener(a)  # Listener joins without delay

    await a.put("First log message")  # Write some logs to channel A
    await a.put("Second log message")  # See them printed, clear as day

    await asyncio.sleep(1)  # A short pause to let them show

    await a.put(None)  # Close A, and end the flow
    await b.put(None)  # And B as well, for the curtain call

# Run the main function
# asyncio.run(main())

# SyntaxError: 'await' outside function ,
#a = await log_scribe()  # Call the scribe to start the play
#b = await log_listener(a)  # Listener joins without delay

# SyntaxError: 'await' outside async function
#def abc():
#    await log_scribe()

# ====== test xonsh
# 坚持去λ化(中-易) jim-emacs-fun-py  master @ asyncio.run(a.put("dasdasdsadsa"))
# 坚持去λ化(中-易) jim-emacs-fun-py  master @ a
# <Queue at 0x13a730b10 maxsize=0 _queue=['dasdasdsadsa'] tasks=4>
# 坚持去λ化(中-易) jim-emacs-fun-py  master @ b
# <Queue at 0x13aa1efd0 maxsize=0 tasks=1>
# 坚持去λ化(中-易) jim-emacs-fun-py  master @  asyncio.run(a.put("dasdasdsadsa321321"))
# 坚持去λ化(中-易) jim-emacs-fun-py  master @ a
# <Queue at 0x13a730b10 maxsize=0 _queue=['dasdasdsadsa', 'dasdasdsadsa321321'] tasks=5>
# 坚持去λ化(中-易) jim-emacs-fun-py  master @  asyncio.run(a.put("dasdasdsadsa321321321312"))
# 坚持去λ化(中-易) jim-emacs-fun-py  master @ a
# <Queue at 0x13a730b10 maxsize=0 _queue=['dasdasdsadsa', 'dasdasdsadsa321321', 'dasdasdsadsa321321321312'] tasks=6>
# 坚持去λ化(中-易) jim-emacs-fun-py  master @ asyncio.run(a.put(None))
# 坚持去λ化(中-易) jim-emacs-fun-py  master @
# 坚持去λ化(中-易) jim-emacs-fun-py  master @ a
# <Queue at 0x13a730b10 maxsize=0 _queue=['dasdasdsadsa', 'dasdasdsadsa321321', 'dasdasdsadsa321321321312', None] tasks=7>
# 坚持去λ化(中-易) jim-emacs-fun-py  master @ b
# <Queue at 0x13aa1efd0 maxsize=0 tasks=1>
# 坚持去λ化(中-易) jim-emacs-fun-py  master @
#

# => 不能打印出来这两个日志
#asyncio.run(a.put("hi a---- steve"))
#asyncio.run(b.put("hi b---- john"))

# GPT修改代码: the Queue a & b is global variables, can put message in anywhere
async def external_put():
    await a.put("Message from outside")

# Somewhere in your code, you would run the external_put function => 还是无效。。。
asyncio.run(external_put())
