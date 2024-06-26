import asyncio
import datetime

async def display_date():
    loop = asyncio.get_running_loop()
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)

asyncio.run(display_date())
# 2024-06-26 22:56:02.237272
# 2024-06-26 22:56:03.238464
# 2024-06-26 22:56:04.239885
# 2024-06-26 22:56:05.241176
# 2024-06-26 22:56:06.242448
#
