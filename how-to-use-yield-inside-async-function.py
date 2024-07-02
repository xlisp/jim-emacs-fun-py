
## https://stackoverflow.com/questions/37549846/how-to-use-yield-inside-async-function
import asyncio

# 删除前面的indent，还会出错，C-c d  TODO => 而且emacs复制进去也出错？？？TODO
async def createGenerator():
    mylist = range(3)
    for i in mylist:
        await asyncio.sleep(1)
        yield i*i # 把循环留给下一个程序，迭代器传递

async def start():
    mygenerator = await createGenerator()
    for i in mygenerator:
        print(i)

# SyntaxError: 'await' outside function, 因为import asyncio?
# await start()
asyncio.run(start()) #=> TypeError: object async_generator can't be used in 'await' expression

# 想起来了，之前看到连for循环都要加async！不然就无法执行。=> 对于调用createGenerator async 函数来说
async def start2():
    async for i in createGenerator():
        print(i)

asyncio.run(start2())
#=>
0
1
4
