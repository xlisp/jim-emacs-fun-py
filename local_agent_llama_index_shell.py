# https://github.com/run-llama/python-agents-tutorial/blob/main/2_local_agent.py
# GPT1:  following this code： XXX run shell code as tools , code return as observe. input quesion can call ipython code tools answer this question "Execute the installation command npm install. If successful, it will return to npm list. If it fails, it will return to node -v."
import os
from dotenv import load_dotenv
load_dotenv()
from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool
# https://langfuse.com/docs/integrations/llama-index/get-started
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from langfuse.llama_index import LlamaIndexCallbackHandler
import subprocess

langfuse_callback_handler = LlamaIndexCallbackHandler()
Settings.callback_manager = CallbackManager([langfuse_callback_handler])

langfuse_callback_handler.set_trace_params(
  user_id="user-123",
  session_id="session-abc",
  tags=["ReAct shell"]
)

def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return a * b
multiply_tool = FunctionTool.from_defaults(fn=multiply)

def add(a: float, b: float) -> float:
    """Add two numbers and returns the sum"""
    return a + b
add_tool = FunctionTool.from_defaults(fn=add)

def run_shell_command(command: str) -> str:
    """Runs a shell command and returns the output or error"""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.stderr.decode('utf-8')
shell_command_tool = FunctionTool.from_defaults(fn=run_shell_command)

llm = Ollama(model="llama3:latest", request_timeout=120.0)

agent = ReActAgent.from_tools([multiply_tool, add_tool, shell_command_tool], llm=llm, verbose=True)

response = agent.chat("Execute the installation command npm install. If successful, it will return to npm list. If it fails, it will return to node -v.")

print(response)

## TODO: 比如问加法和命令的：两个文件夹目录相差多少个文件？

