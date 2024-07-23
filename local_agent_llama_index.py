# https://github.com/run-llama/python-agents-tutorial/blob/main/2_local_agent.py
import os
# prun python local_agent_llama_index.py 可以识别 $LANGFUSE_PUBLIC_KEY 在xonshrc定义变量

# os.environ["LANGFUSE_PUBLIC_KEY"] = "sk-lf-eb90153a-e53f-4997-9d99-4afc840b01ef"
# os.environ["LANGFUSE_SECRET_KEY"] = "pk-lf-63de746a-efed-49ea-af26-d9208853b652"
# os.environ["LANGFUSE_HOST"] = "http://localhost:3000"
# => 本地LANGFUSE key 无效！
#received error response: {'error': 'UnauthorizedError', 'message': "Invalid public key. Confirm that you've configured the correct host."}
#Received 401 error by Langfuse server, not retrying: {'error': 'UnauthorizedError', 'message': "Invalid public key. Confirm that you've configured the correct host."}

# langfuse_us_key() 是有效的 , ！！US的变量是有效的。!!!
# os.environ["LANGFUSE_PUBLIC_KEY"] = 。。。

from dotenv import load_dotenv
load_dotenv()
from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool

# https://langfuse.com/docs/integrations/llama-index/get-started
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from langfuse.llama_index import LlamaIndexCallbackHandler
langfuse_callback_handler = LlamaIndexCallbackHandler()
Settings.callback_manager = CallbackManager([langfuse_callback_handler])

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

## 调用llm的tracing: https://us.cloud.langfuse.com/project/clxfdeck6000fl5tkkzg8ut7r/traces/bc05dc1b-d0e1-41ae-95c7-713a29b2da08
# 坚持去λ化(中-易) jim-emacs-fun-py  master @  prun python local_agent_llama_index.py
# > Running step e1420a7c-c762-45b5-9b00-fb604dbf93ab. Step input: What is 20+(2*4)? Calculate step by step.
# Thought: The current language of the user is English. I need to use a tool to help me answer the question.
# Action: add
# Action Input: {'a': 20, 'b': 8}
# Observation: 28
# > Running step 84e74b95-6aad-460b-8d15-d95a0f3ffa81. Step input: None
# Thought: Now that we know the result of 20+(2*4), let's analyze this step by step. We can use another tool to multiply 2 and 4 first.
# Action: multiply
# Action Input: {'a': 2, 'b': 4}
# Observation: 8
# > Running step 25901cb7-6e1a-4430-8257-801343919c34. Step input: None
# Thought: Now that we know the result of 2*4 is 8. We can substitute this value back into the original equation to get 20+8.
# Action: add
# Action Input: {'a': 20, 'b': 8}
# Observation: 28
# > Running step 6b4201c2-93a9-4df3-a3dd-cc281915cba2. Step input: None
# Thought: I can answer without using any more tools. I'll use the user's language to answer
# Answer: The final result is indeed 28!
# The final result is indeed 28!
# 坚持去λ化(中-易) jim-emacs-fun-py  master @
#
