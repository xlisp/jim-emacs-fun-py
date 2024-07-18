import json

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit", playground=None):
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": "celsius", "playground": str(playground)})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": "fahrenheit", "playground": str(playground)})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": "celsius", "playground": str(playground)})
    else:
        return json.dumps({"location": location, "temperature": "unknown", "playground": str(playground)})

def get_key_point_file(files, playground=None):
    return json.dumps({"key_points": "README.md, package.json ....", "playground": str(playground)})

def get_template(lang, playground=None):
    if "nextjs" in lang.lower():
        return json.dumps({"template": "NEXTJS_SHELL_BACKGROUND", "playground": str(playground)})
    if "go" in lang.lower():
        return json.dumps({"template": "GO_GIN_SHELL_BACKGROUND", "playground": str(playground)})
    if "java" in lang.lower():
        return json.dumps({"template": "JAVA_SHELL_BACKGROUND", "playground": str(playground)})
    if "html" in lang.lower():
        return json.dumps({"template": "HTML_CSS_JS_SHELL_BACKGROUND", "playground": str(playground)})

def get_env_info(lang, playground=None):
    if "nextjs" in lang.lower():
        return json.dumps({"env_info": "TODO: npm list ENV...", "playground": str(playground)})
    if "go" in lang.lower():
        return json.dumps({"env_info": "TODO: go libs ENV...", "playground": str(playground)})
    if "java" in lang.lower()):
        return json.dumps({"env_info": "TODO: mvn tree ENV...", "playground": str(playground)})
    if "html" in lang.lower()):
        return json.dumps({"env_info": "TODO: node ENV...", "playground": str(playground)})

def test_parallel_function_call(playground):
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
                            "playground": {"type": "object"}
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
                            "playground": {"type": "object"}
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
                            "playground": {"type": "object"}
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
                            "playground": {"type": "object"}
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
                    **function_args,
                    playground=playground
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
playground = {"example_key": "example_value"}
test_parallel_function_call(playground)

