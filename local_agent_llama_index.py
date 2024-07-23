# https://github.com/run-llama/python-agents-tutorial/blob/main/2_local_agent.py
from dotenv import load_dotenv
load_dotenv()
from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool

def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return a * b

multiply_tool = FunctionTool.from_defaults(fn=multiply)

def add(a: float, b: float) -> float:
    """Add two numbers and returns the sum"""
    return a + b

add_tool = FunctionTool.from_defaults(fn=add)

#llm = Ollama(model="mixtral:8x7b", request_timeout=120.0) => 26GB太大了
llm = Ollama(model="llama3:latest", request_timeout=120.0)

agent = ReActAgent.from_tools([multiply_tool, add_tool], llm=llm, verbose=True)

response = agent.chat("What is 20+(2*4)? Calculate step by step.")

print(response) #=> Answer: The result of 20+(2*4) is 28.

# In [1]: from dotenv import load_dotenv
# from dotenv import load_dotenvIn [1]: from dotenv import load_dotenv
#
# In [2]: load_dotenv()
# In [2]: load_dotenv()
# Out[2]: False
#
# In [3]: from llama_index.core.agent import ReActAgent
# from llama_index.core.agent import ReActAgentIn [3]: from llama_index.core.agent import ReActAgent
#
# In [4]: from llama_index.llms.ollama import Ollama
# In [4]: from llama_index.llms.ollama import Ollama
#
# In [5]: from llama_index.core.tools import FunctionTool
# from llama_index.core.tools import FunctionToolIn [5]: from llama_index.core.tools import FunctionTool
#
# In [6]:
# def multiply(a: float, b: float) -> float:
# """Multiply two numbers and returns the product"""
# return a * b
#
#
#
# In [6]: In [6]:
#
# In [6]: def multiply(a: float, b: float) -> float:
#    ...:     """Multiply two numbers and returns the product"""
#    ...:     return a * b
#    ...: In [6]: def multiply(a: float, b: float) -> float:
#    ...:     """Multiply two numbers and returns the product"""
#    ...:     return a * b
#    ...:
#
# In [7]: In [7]:
#
# In [7]: In [7]:
#
# In [7]: In [7]: In [7]:
# multiply_tool = FunctionTool.from_defaults(fn=multiply)
#
#
#
# In [7]: In [7]:
#
# In [7]: multiply_tool = FunctionTool.from_defaults(fn=multiply)In [7]: multiply_tool = FunctionTool.from_defaults(fn=multiply)
#
# In [8]: In [8]:
#
# In [8]: In [8]:
#
# In [8]: In [8]:
#
# In [8]: In [8]: In [8]:
# def add(a: float, b: float) -> float:
# """Add two numbers and returns the sum"""
# return a + b
#
#
#
# In [8]: In [8]:
#
# In [8]: def add(a: float, b: float) -> float:
#    ...:     """Add two numbers and returns the sum"""
#    ...:     return a + b
#    ...: In [8]: def add(a: float, b: float) -> float:
#    ...:     """Add two numbers and returns the sum"""
#    ...:     return a + b
#    ...:
#
# In [9]: In [9]:
#
# In [9]: In [9]:
#
# In [9]: In [9]: In [9]:
# In [9]:
#
# In [9]: add
# In [9]: add
# Out[9]: <function __main__.add(a: float, b: float) -> float>
#
# In [10]: multiply
# In [10]: multiply
# Out[10]: <function __main__.multiply(a: float, b: float) -> float>
#
# In [11]: add_tool = FunctionTool.from_defaults(fn=add)
# In [11]: add_tool = FunctionTool.from_defaults(fn=add)
#
# In [12]: llm = Ollama(model="llama3:latest", request_timeout=120.0)
# llm = Ollama(model="llama3:latest", request_timeout=120.0)In [12]: llm = Ollama(model="llama3:latest", request_timeout=120.0)
#
# In [13]: agent = ReActAgent.from_tools([multiply_tool, add_tool], llm=llm, verbose=True)
# )
# )
#     ...:
#
# In [14]: response = agent.chat("What is 20+(2*4)? Calculate step by step.")
# response = agent.chat("What is 20+(2*4)? Calculate step by step.")In [14]: response = agent.chat("What is 20+(2*4)? Calculate step by step.")
# > Running step b87b02fe-c498-44a4-9781-47f817b4ebf0. Step input: What is 20+(2*4)? Calculate step by step.
# Thought: The current language of the user is: English. I need to use a tool to help me answer the question.
# Action: add
# Action Input: {'a': 20, 'b': AttributedDict([('input', 8), ('type', 'number')])}
# Observation: Error: unsupported operand type(s) for +: 'int' and 'AttributedDict'
# > Running step 359de45a-775e-43e3-8f68-1a0e756ea2b0. Step input: None
# Thought: It seems like the tool I used earlier didn't work as expected. Let me try again.
# Action: multiply
# Action Input: {'a': 2, 'b': 4}
# Observation: 8
# > Running step ece4f5fe-8036-41bb-9c84-6d39c5d3a2cd. Step input: None
# Thought: Now that I have the result of 2*4, I can continue with the original question. Time to use another tool!
# Action: add
# Action Input: {'a': 20, 'b': 8}
# Observation: 28
# > Running step 905a5e8e-3bd4-4c94-8a2b-301143e4d195. Step input: None
# Thought: The calculation is complete! Now I can provide the final answer.
# Answer: The result of 20+(2*4) is 28.
# In [15]:
#
#
