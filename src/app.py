from flask import Flask
from routes import main_router
from flask_wtf import CSRFProtect

from flask_socketio import SocketIO, send, emit
import os
from datetime import datetime


app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

app.register_blueprint(main_router.main_router, url_prefix='/')

csrf = CSRFProtect()
csrf.init_app(app)


def log_socket(message):
    with open(f'{os.getcwd()}/logs/socket.log', 'a') as f:
        f.write(f'{datetime.now()} - {message}\n')


socketio = SocketIO(app, cors_allowed_origins="*")
@socketio.on('connect')
def handle_connect():
    log_socket(f'[CLIENT CONNECTED]')

@socketio.on('disconnect')
def handle_disconnect():
    log_socket(f'[CLIENT DISCONNECTED]')


@socketio.on('message')
def handle_message(msg):
    log_socket(f'[MESSAGE] {msg}')

@socketio.on('json')
def handle_json(json):
    print(f'[JSON MESSAGE] {str(json)}')



if __name__ == '__main__':
    socketio.run(app, host=os.getenv('HOST'), port=os.getenv('PORT'), ssl_context=('../cert.pem', '../key.pem'), debug=True) # certificates for https