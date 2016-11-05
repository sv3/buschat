#!/usr/bin/env python
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supercalifragilistic'
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app) 
thread = None

with open('history.txt') as histfile:
    history = histfile.readlines()

print history

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html', async_mode=socketio.async_mode,
	   hist=history)


@socketio.on('my_broadcast_event')
def test_broadcast_message(message):
    print message
    #history.append('\n{}: {}'.format(message['name'], message['message']))
    emit('my_response', {'message': message['data']}, broadcast=True)


@socketio.on('disconnect_request')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('my_ping')
def ping_pong():
    emit('my_pong')


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
