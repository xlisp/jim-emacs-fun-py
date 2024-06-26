import asyncio

task = asyncio.create_task(something())
try:
    res = await asyncio.shield(task) #=> SyntaxError: 'await' outside function
except CancelledError:
    res = None
