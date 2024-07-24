import os
from dotenv import load_dotenv
load_dotenv()
from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from langfuse.llama_index import LlamaIndexCallbackHandler
import subprocess

from flask import Flask, request
from flask_socketio import SocketIO, send

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Set up the Langfuse callback handler
langfuse_callback_handler = LlamaIndexCallbackHandler()
Settings.callback_manager = CallbackManager([langfuse_callback_handler])

langfuse_callback_handler.set_trace_params(
  user_id="user-123",
  session_id="session-abc",
  tags=["ReAct shell"]
)

# Define the functions to be used as tools
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

# Initialize the LLM and agent
llm = Ollama(model="llama3.1:latest", request_timeout=120.0)
agent = ReActAgent.from_tools([multiply_tool, add_tool, shell_command_tool], llm=llm, verbose=True)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    if message == "connect":
        send("Welcome to the chat!")
    else:
        response = agent.chat(message)
        send(response)

# Start the Flask server with SocketIO
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=6000)


## ----- log
# 坚持去λ化(中-易) jim-emacs-fun-py  master @ prun python llama_index_shell_server.py
#  * Serving Flask app 'llama_index_shell_server'
#  * Debug mode: off
# WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
#  * Running on all addresses (0.0.0.0)
#  * Running on http://127.0.0.1:6000
#  * Running on http://198.18.0.1:6000
# Press CTRL+C to quit
# 127.0.0.1 - - [24/Jul/2024 12:13:06] "GET /socket.io/?transport=polling&EIO=4&t=1721794386.253651 HTTP/1.1" 200 -
# 127.0.0.1 - - [24/Jul/2024 12:13:06] "POST /socket.io/?transport=polling&EIO=4&sid=cK4KXE3TJ1tjqD4UAAAA HTTP/1.1" 200 -
# 127.0.0.1 - - [24/Jul/2024 12:13:06] "GET /socket.io/?transport=polling&EIO=4&sid=cK4KXE3TJ1tjqD4UAAAA&t=1721794386.257666 HTTP/1.1" 200 -
# received message: connect
# 127.0.0.1 - - [24/Jul/2024 12:13:06] "POST /socket.io/?transport=polling&EIO=4&sid=cK4KXE3TJ1tjqD4UAAAA HTTP/1.1" 200 -
# 127.0.0.1 - - [24/Jul/2024 12:13:06] "GET /socket.io/?transport=polling&EIO=4&sid=cK4KXE3TJ1tjqD4UAAAA&t=1721794386.259975 HTTP/1.1" 200 -
# received message: Execute the installation command npm install. If successful, it will return to npm list. If it fails, it will return to node -v.
# 127.0.0.1 - - [24/Jul/2024 12:13:06] "POST /socket.io/?transport=polling&EIO=4&sid=cK4KXE3TJ1tjqD4UAAAA HTTP/1.1" 200 -
# > Running step 38c1894e-b7da-4091-9cc6-7425842c426d. Step input: Execute the installation command npm install. If successful, it will return to npm list. If it fails, it will return to node -v.
# Thought: The user wants to execute a shell command and check its output or error. I need to use the run_shell_command tool.
# Action: run_shell_command
# Action Input: {'command': 'npm install'}
# Observation: npm error code ENOENT
# npm error syscall open
# npm error path /Users/emacspy/EmacsPyPro/jim-emacs-fun-py/package.json
# npm error errno -2
# npm error enoent Could not read package.json: Error: ENOENT: no such file or directory, open '/Users/emacspy/EmacsPyPro/jim-emacs-fun-py/package.json'
# npm error enoent This is related to npm not being able to find a file.
# npm error enoent
# npm error A complete log of this run can be found in: /Users/emacspy/.npm/_logs/2024-07-24T04_13_25_947Z-debug-0.log
# 
# > Running step 94837f88-6bd5-4bdf-baff-254723d0b600. Step input: None
# 127.0.0.1 - - [24/Jul/2024 12:13:31] "GET /socket.io/?transport=polling&EIO=4&sid=cK4KXE3TJ1tjqD4UAAAA&t=1721794386.262482 HTTP/1.1" 200 -
# 127.0.0.1 - - [24/Jul/2024 12:13:31] "POST /socket.io/?transport=polling&EIO=4&sid=cK4KXE3TJ1tjqD4UAAAA HTTP/1.1" 200 -
# Thought: The user's npm install command failed due to an ENOENT error, which is related to not being able to find a package.json file. This suggests that the current working directory might not be as expected. I need to use the run_shell_command tool again.
# Action: run_shell_command
# Action Input: {'command': 'pwd'}
# Observation: /Users/emacspy/EmacsPyPro/jim-emacs-fun-py
# 
# > Running step 6953941b-c70e-4030-9227-c8f62d36ac5f. Step input: None
# Thought: The user's current working directory is /Users/emacspy/EmacsPyPro/jim-emacs-fun-py. I need to use the run_shell_command tool again to check if there's a package.json file in this directory.
# Action: run_shell_command
# Action Input: {'command': 'ls package.json'}
# Observation: ls: package.json: No such file or directory
# 
# > Running step 44b27617-0908-478e-ac77-1d182ba8a9bc. Step input: None
# Thought: There is no package.json file in the current working directory. This explains why the npm install command failed earlier. I need to use the run_shell_command tool again to try a different command.
# Action: run_shell_command
# Action Input: {'command': 'node -v'}
# Observation: v22.3.0
# 
# > Running step 05f8941f-4b7d-4447-969d-dc4280a96c16. Step input: None
# Thought: The user's Node.js version is 22.3.0. Since the npm install command failed earlier and there's no package.json file in the current working directory, I can now safely assume that the installation command was not relevant to the overall conversation. I have enough information to provide a final answer.
# Answer: There is no package.json file in the current working directory, so there's nothing to install with npm. The Node.js version is 22.3.0, which seems to be installed and functional.
# Exception in thread Thread-12 (_handle_event_internal):
# Traceback (most recent call last):
#   File "/opt/anaconda3/lib/python3.11/threading.py", line 1045, in _bootstrap_inner
#     self.run()
#   File "/opt/anaconda3/lib/python3.11/threading.py", line 982, in run
#     self._target(*self._args, **self._kwargs)
#   File "/Users/emacspy/Library/Caches/pypoetry/virtualenvs/jim-emacs-fun-py-LpKaBAU7-py3.11/lib/python3.11/site-packages/socketio/server.py", line 589, in _handle_event_internal
#     r = server._trigger_event(data[0], namespace, sid, *data[1:])
#         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Users/emacspy/Library/Caches/pypoetry/virtualenvs/jim-emacs-fun-py-LpKaBAU7-py3.11/lib/python3.11/site-packages/socketio/server.py", line 614, in _trigger_event
#     return handler(*args)
#            ^^^^^^^^^^^^^^
#   File "/Users/emacspy/Library/Caches/pypoetry/virtualenvs/jim-emacs-fun-py-LpKaBAU7-py3.11/lib/python3.11/site-packages/flask_socketio/__init__.py", line 282, in _handler
#     return self._handle_event(handler, message, namespace, sid,
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Users/emacspy/Library/Caches/pypoetry/virtualenvs/jim-emacs-fun-py-LpKaBAU7-py3.11/lib/python3.11/site-packages/flask_socketio/__init__.py", line 827, in _handle_event
#     ret = handler(*args)
#           ^^^^^^^^^^^^^^
#   File "/Users/emacspy/EmacsPyPro/jim-emacs-fun-py/llama_index_shell_server.py", line 61, in handle_message
#     send(response)
#   File "/Users/emacspy/Library/Caches/pypoetry/virtualenvs/jim-emacs-fun-py-LpKaBAU7-py3.11/lib/python3.11/site-packages/flask_socketio/__init__.py", line 1007, in send
#     return socketio.send(message, json=json, namespace=namespace, to=to,
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Users/emacspy/Library/Caches/pypoetry/virtualenvs/jim-emacs-fun-py-LpKaBAU7-py3.11/lib/python3.11/site-packages/flask_socketio/__init__.py", line 537, in send
#     self.emit('message', data, namespace=namespace, to=to,
#   File "/Users/emacspy/Library/Caches/pypoetry/virtualenvs/jim-emacs-fun-py-LpKaBAU7-py3.11/lib/python3.11/site-packages/flask_socketio/__init__.py", line 462, in emit
#     self.server.emit(event, *args, namespace=namespace, to=to,
#   File "/Users/emacspy/Library/Caches/pypoetry/virtualenvs/jim-emacs-fun-py-LpKaBAU7-py3.11/lib/python3.11/site-packages/socketio/server.py", line 166, in emit
#     self.manager.emit(event, data, namespace, room=room,
#   File "/Users/emacspy/Library/Caches/pypoetry/virtualenvs/jim-emacs-fun-py-LpKaBAU7-py3.11/lib/python3.11/site-packages/socketio/manager.py", line 43, in emit
#     encoded_packet = pkt.encode()
#                      ^^^^^^^^^^^^
#   File "/Users/emacspy/Library/Caches/pypoetry/virtualenvs/jim-emacs-fun-py-LpKaBAU7-py3.11/lib/python3.11/site-packages/socketio/packet.py", line 64, in encode
#     encoded_packet += self.json.dumps(data, separators=(',', ':'))
#                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/opt/anaconda3/lib/python3.11/json/__init__.py", line 238, in dumps
#     **kw).encode(obj)
#           ^^^^^^^^^^^
#   File "/opt/anaconda3/lib/python3.11/json/encoder.py", line 200, in encode
#     chunks = self.iterencode(o, _one_shot=True)
#              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/opt/anaconda3/lib/python3.11/json/encoder.py", line 258, in iterencode
#     return _iterencode(o, 0)
#            ^^^^^^^^^^^^^^^^^
#   File "/opt/anaconda3/lib/python3.11/json/encoder.py", line 180, in default
#     raise TypeError(f'Object of type {o.__class__.__name__} '
# TypeError: Object of type AgentChatResponse is not JSON serializable
# 127.0.0.1 - - [24/Jul/2024 12:13:56] "GET /socket.io/?transport=polling&EIO=4&sid=cK4KXE3TJ1tjqD4UAAAA&t=1721794411.269233 HTTP/1.1" 200 -
# 
