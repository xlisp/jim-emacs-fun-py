import litellm
import asyncio

from litellm import acompletion

async def test_get_response_stream(q):
    user_message = q #"Hello, how are you?"
    messages = [{"content": user_message, "role": "user"}]
    response = await acompletion(model="gpt-3.5-turbo", messages=messages, stream=True)
    # return response
    res = ''
    async def ws_send(word):
        # await print(word) ## 只能await async过来的对象：TypeError: object NoneType can't be used in 'await' expression
        print(word)
    # for chunk in response: ## 无法直接取出，是一个队列对象，TypeError: 'AsyncStream' object is not an iterator
    async for chunk in response:
        word = chunk.choices[0].delta.content or ''
        res = res + word
        #await print(word, end='', flush=True) ## TypeError: object NoneType can't be used in 'await' expression
        await ws_send(res)

asyncio.run(test_get_response_stream("hi"))

# => 
# Hello
# Hello!
# Hello! How
# Hello! How can
# Hello! How can I
# Hello! How can I assist
# Hello! How can I assist you
# Hello! How can I assist you today
# Hello! How can I assist you today?
# Hello! How can I assist you today?
# 
