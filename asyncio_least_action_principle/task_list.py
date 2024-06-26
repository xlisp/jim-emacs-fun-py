import asyncio

background_tasks = set()

async def some_coro(param):
    return param

for i in range(10):
    task = asyncio.create_task(some_coro(1))

    # Add task to the set. This creates a strong reference.
    background_tasks.add(task)

    # To prevent keeping references to finished tasks forever,
    # make each task remove its own reference from the set after
    # completion:
    task.add_done_callback(background_tasks.discard)

# RuntimeError: no running event loop
# sys:1: RuntimeWarning: coroutine 'some_coro' was never awaited
#
