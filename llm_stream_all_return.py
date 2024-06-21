# https://github.com/BerriAI/litellm-staging
from litellm import acompletion
import asyncio
# print(asyncio.run(test_get_response(q))) => ModelResponse(id='chatcmpl-9cRAjj55YDmx94BNkLdos2Vyh7Rb5', choices=[Choices(finish_reason='stop', index=0, message=Message(content='Hello! How can I help you today?', role='assistant'))], created=1718947941, model='gpt-3.5-turbo-0125', object='chat.completion', system_fingerprint=None, usage=Usage(completion_tokens=9, prompt_tokens=8, total_tokens=17))
async def test_get_response(q):
    user_message = q #"Hello, how are you?"
    messages = [{"content": user_message, "role": "user"}]
    response = await acompletion(model="gpt-3.5-turbo", messages=messages)
    return response

print(asyncio.run(test_get_response("hi")))
