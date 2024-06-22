import asyncio
from asyncio import Queue

# Global queues
a = Queue()
b = Queue()

async def log_scribe():
    async def logging_loop():
        while True:
            msg = await a.get()
            if msg is None:
                break
            print("Logging:", msg)

    asyncio.create_task(logging_loop())

async def log_listener():
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

async def main():
    await log_scribe()  # Start the logging loop
    await log_listener()  # Start the listener and forwarder

    # Write some logs to channel A
    await a.put("First log message")
    await a.put("Second log message")

    await asyncio.sleep(1)  # A short pause to let them show

    # Example of putting messages from an external function
    await external_put()

    await a.put(None)  # Close A, and end the flow
    await b.put(None)  # And B as well, for the curtain call

async def external_put():
    await a.put("Message from outside")
    await asyncio.sleep(0.5)  # Simulate some delay
    await a.put("Another message from outside")

# Run the main function
asyncio.run(main())

