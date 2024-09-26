import openai # openai v1.0.0+
client = openai.OpenAI(api_key="anything",base_url="http://192.168.1.50:4000") # set proxy to base_url
# request sent to model set on litellm proxy, `litellm --model`
response = client.chat.completions.create(model="gpt-3.5-turbo", messages = [
    {
        "role": "user",
        "content": "this is a test request, write a short poem"
    }
])

print(response)

## run -----
# ChatCompletion(id='chatcmpl-b7a1a911-991d-45c6-9a09-c2d231075519', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content="A whisper of wind through leaves so green,\nA sunbeam dances, a joyful scene.\nA robin sings, a melody bright,\nThis simple moment, a pure delight. \n\n\nLet me know if you'd like another poem on a different topic!  😊  \n", refusal=None, role='assistant', function_call=None, tool_calls=None))], created=1727337199, model='ollama/gemma2:9b', object='chat.completion', service_tier=None, system_fingerprint=None, usage=CompletionUsage(completion_tokens=59, prompt_tokens=24, total_tokens=83, completion_tokens_details=None))

