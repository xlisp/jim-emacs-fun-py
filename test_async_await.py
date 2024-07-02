import time


async def ws_send(word):
    print(f"=====ws_send==={time.asctime()}")
    time.sleep(3)
    print(f"----{word}----{time.asctime()}")
    return 123

# 开了python repl就不行，ipython和pdb都是正常的
def ws_send2(word):
    print("=====ws_send===")
    time.sleep(3)
    print(word)


res = await ws_send(1111)

# => 终于可以很好测试 python -m asyncio => ipython也能执行await ws_send(1111)了。 最终才能获得res 123
# >>> await ws_send(1111)
# =====ws_send===Wed Jul  3 00:57:51 2024
# ----1111----Wed Jul  3 00:57:54 2024
# >>>
