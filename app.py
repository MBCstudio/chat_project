# app.py

from flask import Flask, render_template
from flask_socketio import SocketIO, send
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Thread-safe lock for managing messages
message_lock = threading.Lock()
messages = []

@app.route('/')
def index():
    return render_template('chat.html')

# Handle incoming messages
@socketio.on('message')
def handle_message(msg):
    with message_lock:  # Ensure thread-safe access
        messages.append(msg)
        print(f"Message received: {msg}")
    send(msg, broadcast=True)  # Send to all clients

if __name__ == '__main__':
    print("Starting chat server...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
