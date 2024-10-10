from flask import Flask, render_template
from flask_socketio import SocketIO, send
import subprocess

app = Flask(__name__)
socketio = SocketIO(app)

# Serve the HTML page from the `templates` folder
@app.route('/')
def index():
    return render_template('client_terminal.html')

# Socket.IO event listener for incoming messages (commands)
@socketio.on('message')
def handle_message(command):
    try:
        # Run the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        send(result.stdout if result.stdout else "No output")
    except Exception as e:
        send(f"Error: {str(e)}")

if __name__ == '__main__':
    socketio.run(app, host='localhost', port=5001)
