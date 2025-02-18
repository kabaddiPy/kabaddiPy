from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with an actual secret key
socketio = SocketIO(app, async_mode='eventlet')

from app import routes, websocket_handler
