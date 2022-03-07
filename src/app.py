from flask import Flask
from routes import main_router
from flask_wtf import CSRFProtect

from flask_socketio import SocketIO, send, emit # https://socket.io/docs/v3/, https://flask-socketio.readthedocs.io/en/latest/intro.html
import os
from datetime import datetime


app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

app.register_blueprint(main_router.main_router, url_prefix='/')

csrf = CSRFProtect()
csrf.init_app(app)

def log_socket(message=''):
    with open(f'{os.getcwd()}/logs/socket.log', 'a') as f:
        f.write(f'{datetime.now()} - {message}\n')

def log_chat(msg='', user='', ip=''):
    with open(f'{os.getcwd()}/logs/chat.log', 'a') as f:
        f.write(f'[{datetime.now()}|{user}|{ip}]::{msg}\n')

def getAllChatLogs():
    msgs = []
    users = []
    with open(f'{os.getcwd()}/logs/chat.log', 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        for line in lines:
            split = line.split('::')

            msg = split[1]
            user = split[0].split('|')[1]

            msgs.append(msg)
            users.append(user)
    
    return msgs, users

socketio = SocketIO(app, cors_allowed_origins="*")
@socketio.on('connect')
def handle_connect():
    log_socket(f'[CLIENT CONNECTED]')

    chatLogs = getAllChatLogs()
    emit('connect', { 'msgs': chatLogs[0], 'users': chatLogs[1]}) # on connect, send all messages

@socketio.on('disconnect')
def handle_disconnect():
    log_socket(f'[CLIENT DISCONNECTED]')


@socketio.on('message')
def handle_message(msg):
    log_socket(f'[MESSAGE] {msg}')

@socketio.event
def user_message(msg, user, ip):
    log_chat(msg, user, ip)
    emit('user_message', { 'msg': msg, 'user': user }, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host=os.getenv('HOST'), port=os.getenv('PORT'), ssl_context=('../cert.pem', '../key.pem'), debug=True) # certificates for https