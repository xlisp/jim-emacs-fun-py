import asyncio
from asyncio import Queue
import aiochan as ac

a = Queue()

print(a)
# => <Queue maxsize=0>

c = ac.Chan()

print(c)
# => Chan<_unk_0 4379970704>

