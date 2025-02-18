from app import socketio
from flask_socketio import emit
from app.data_fetch import get_live_scores

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connected', {'message': 'Connected to the server'})

@socketio.on('request_live_data')
def handle_live_data_request():
    live_data = get_live_scores()
    emit('live_data', live_data)
