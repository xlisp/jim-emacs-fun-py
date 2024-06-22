import asyncio
from asyncio import Queue

async def log_scribe():
    a = Queue()  # Our channel A, the log's main door

    async def logging_loop():
        while True:
            msg = await a.get()
            if msg is None:
                break
            print("Logging:", msg)

    asyncio.create_task(logging_loop())
    return a

async def log_listener(a):
    b = Queue()  # Channel B, to hear and see

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
asyncio.run(main())
