import litellm
import json
import os

# https://litellm.vercel.app/docs/completion/function_call

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": "celsius"})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": "fahrenheit"})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": "celsius"})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})


def test_parallel_function_call():
    try:
        # Step 1: send the conversation and available functions to the model
        messages = [{"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris?"}]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
                },
            }
        ]
        response = litellm.completion(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            tools=tools,
            tool_choice="auto",  # auto is default, but we'll be explicit
        )
        print("\nFirst LLM Response:\n", response)
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        print("\nLength of tool calls", len(tool_calls))

        # Step 2: check if the model wanted to call a function
        if tool_calls:
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "get_current_weather": get_current_weather,
            }  # only one function in this example, but you can have multiple
            messages.append(response_message)  # extend conversation with assistant's reply

            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(
                    location=function_args.get("location"),
                    unit=function_args.get("unit"),
                )
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            second_response = litellm.completion(
                model="gpt-3.5-turbo-1106",
                messages=messages,
            )  # get a new response from the model where it can see the function response
            print("\nSecond LLM response:\n", second_response)
            return second_response
    except Exception as e:
      print(f"Error occurred: {e}")

test_parallel_function_call()

# First LLM Response:
#  ModelResponse(id='chatcmpl-9cvTuJzxTb7YOyskpMCQpL2m0L9Ph', choices=[Choices(finish_reason='tool_calls', index=0, message=Message(content=None, role='assistant', tool_calls=[ChatCompletionMessageToolCall(function=Function(arguments='{"location": "San Francisco, CA", "unit": "celsius"}', name='get_current_weather'), id='call_FxEx2tHfsSXE4bB2CnOMlkyC', type='function'), ChatCompletionMessageToolCall(function=Function(arguments='{"location": "Tokyo, Japan", "unit": "celsius"}', name='get_current_weather'), id='call_5TDYpjQnC5BOx70VyuSLKvIw', type='function'), ChatCompletionMessageToolCall(function=Function(arguments='{"location": "Paris, France", "unit": "celsius"}', name='get_current_weather'), id='call_yPp8Nnag4P8CIC0VH74GkrMv', type='function')]))], created=1719064450, model='gpt-3.5-turbo-1106', object='chat.completion', system_fingerprint='fp_3d37c73133', usage=Usage(completion_tokens=83, prompt_tokens=88, total_tokens=171))
# 
# Length of tool calls 3
# 
# Second LLM response:
#  ModelResponse(id='chatcmpl-9cvTv5FEUdVnNr5q6xGLyhZ4CGtuh', choices=[Choices(finish_reason='stop', index=0, message=Message(content='Currently in San Francisco, the weather is 72°F. In Tokyo, the weather is 10°C, and in Paris, the weather is 22°C.', role='assistant'))], created=1719064451, model='gpt-3.5-turbo-1106', object='chat.completion', system_fingerprint='fp_3d37c73133', usage=Usage(completion_tokens=33, prompt_tokens=175, total_tokens=208))
# 
