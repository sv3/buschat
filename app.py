#!/usr/bin/env python
import io
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, send, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supercalifragilistic'
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app) 
### DELETE?
thread = None


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        try:
            with io.open('history.txt') as histfile:
                history = [ line.rstrip().split(':',1) for line in histfile ]
        except IOError as e:
            history = ''
        return render_template('index.html', async_mode=socketio.async_mode,hist=history)
    else: return ('', 204)


@socketio.on('message')
def broadcast_message(msg):
    print msg
    if not(msg['name']) or msg['name'].isspace():
        msg['name'] = 'anonymous'
    entry = u'{}: {}\n'.format(msg['name'], msg['message'])
    with io.open('history.txt', 'a') as histfile:
        histfile.write(entry)
    send(msg, broadcast=True)


@socketio.on('disconnect_request')
def disconnect_request():
    emit('my_response', ['','Disconnected!'])
    disconnect()


@socketio.on('my_ping')
def ping_pong():
    emit('my_pong')


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
