import litellm
import json
import os

import json

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

def get_key_point_file(files):
    return "README.md, package.json ...."

def get_template(lang):
    if "nextjs" in lang.lower():
        return "NEXTJS_SHELL_BACKGROUND"
    if "go" in lang.lower():
        return "GO_GIN_SHELL_BACKGROUND"
    if "java" in lang.lower():
        return "JAVA_SHELL_BACKGROUND"
    if "html" in lang.lower():
        return "HTML_CSS_JS_SHELL_BACKGROUND"

def get_env_info(lang):
    if "nextjs" in lang.lower():
        return "TODO: npm list ENV..."
    if "go" in lang.lower():
        return "TODO: go libs ENV..."
    if "java" in lang.lower():
        return "TODO: mvn tree ENV..."
    if "html" in lang.lower():
        return "TODO: node ENV..."

def test_parallel_function_call():
    try:
        # Step 1: send the conversation and available functions to the model
        messages = [{"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris? Can you also get the key points of the files and the templates and environment info for NextJS?"}]
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
            },
            {
                "type": "function",
                "function": {
                    "name": "get_key_point_file",
                    "description": "Get key point file information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "files": {
                                "type": "string",
                                "description": "A list of files",
                            },
                        },
                        "required": ["files"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_template",
                    "description": "Get the template for a given language",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lang": {
                                "type": "string",
                                "description": "The programming language or framework",
                            },
                        },
                        "required": ["lang"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_env_info",
                    "description": "Get environment info for a given language",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lang": {
                                "type": "string",
                                "description": "The programming language or framework",
                            },
                        },
                        "required": ["lang"],
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
                "get_key_point_file": get_key_point_file,
                "get_template": get_template,
                "get_env_info": get_env_info,
            }  # multiple functions in this example
            messages.append(response_message)  # extend conversation with assistant's reply

            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(
                    **function_args
                )
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool", ## Assistant API 支持三种 工具：代码解释器（Code Interpreter）、信息检索（Retrieval）和函数调用（Function calling） 。=> Function calling是tools属性。
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

# Example usage
test_parallel_function_call()

# First LLM Response:
#  ModelResponse(id='chatcmpl-9m1j9yOyhU6sBpEHnBrLY7OXiKalo', choices=[Choices(finish_reason='tool_calls', index=0, message=Message(content=None, role='assistant', tool_calls=[ChatCompletionMessageToolCall(function=Function(arguments='{"location": "San Francisco", "unit": "celsius"}', name='get_current_weather'), id='call_TDrBVBkRAkMV3yciZKmJ8HQ2', type='function'), ChatCompletionMessageToolCall(function=Function(arguments='{"location": "Tokyo", "unit": "celsius"}', name='get_current_weather'), id='call_GAm6tnBtnRSYM2fQymgsH6rs', type='function'), ChatCompletionMessageToolCall(function=Function(arguments='{"location": "Paris", "unit": "celsius"}', name='get_current_weather'), id='call_gkC8EYNgw5ZyhH8pZzba5Djj', type='function'), ChatCompletionMessageToolCall(function=Function(arguments='{"files": "file1.txt, file2.md, file3.js"}', name='get_key_point_file'), id='call_Q8RQZ91iXtYCqUujRqzyxhV8', type='function'), ChatCompletionMessageToolCall(function=Function(arguments='{"lang": "NextJS"}', name='get_template'), id='call_bB45MveUPjbUc2SJRfnPZC7z', type='function'), ChatCompletionMessageToolCall(function=Function(arguments='{"lang": "NextJS"}', name='get_env_info'), id='call_xt8YgmM9MbnVQu2QMeUcVaRB', type='function')]))], created=1721233411, model='gpt-3.5-turbo-1106', object='chat.completion', system_fingerprint='fp_0ccba42292', usage=Usage(completion_tokens=134, prompt_tokens=201, total_tokens=335))

# Length of tool calls 6

# Second LLM response:
#  ModelResponse(id='chatcmpl-9m1jCS4K2SGe3CrMYfCnnMFNO5StE', choices=[Choices(finish_reason='stop', index=0, message=Message(content='The current weather is as follows:\n- San Francisco: 72°F\n- Tokyo: 10°C\n- Paris: 22°C\n\nThe key points of the files are in "README.md, package.json, etc." and the template and environment information for NextJS are in the NextJS shell background and the npm list environment.', role='assistant'))], created=1721233414, model='gpt-3.5-turbo-1106', object='chat.completion', system_fingerprint='fp_0ccba42292', usage=Usage(completion_tokens=68, prompt_tokens=268, total_tokens=336))

