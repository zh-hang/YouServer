import sqlite3
import json

from . import db, app_socket_io
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app)
from werkzeug.security import (check_password_hash, generate_password_hash)

chatroom_bp = Blueprint('chatroom', __name__, url_prefix='/chatroom')


class Chatroom:
    def __init__(self, chatroom_id_int, chatroom_name_string):
        self.id_int = chatroom_id_int
        self.name_string = chatroom_name_string
        self.people_number_int = 0

    def getinfo(self):
        return {'id': self.id_int, 'name': self.name_string, 'people_number': self.people_number_int}

    def __eq__(self, other_chatroom):
        return self.id_int == other_chatroom.id_int

    def __str__(self):
        return '{"id":' + str(self.id_int) + ',"name":' + self.name_string + ',"people_number":' + str(
            self.people_number_int) + '}'


class ChatroomResource:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print('something wrong')
        else:
            print('everything fine')

    @staticmethod
    def getChatroomLists():
        chatroom_db = sqlite3.connect('./instance/you.db')
        chatroom_db_lists = chatroom_db.execute(
            'SELECT * FROM chatroom').fetchall()
        print(chatroom_db_lists)
        chatroom_temp_lists = []
        for i in chatroom_db_lists:
            chatroom_temp_lists.append(Chatroom(i[0], i[1]))
        chatroom_db.close()
        return chatroom_temp_lists


chatroom_lists = []
try:
    with ChatroomResource() as resource:
        chatroom_lists = resource.getChatroomLists()
except Exception as e:
    print(e)


def modify_chatroom_number(chatroom_id_int, is_in_bool):
    for i in chatroom_lists:
        if i.id_int == chatroom_id_int:
            if is_in_bool:
                i.people_number_int += 1
            else:
                i.people_number_int -= 1


@app_socket_io.on('connect')
def test_connect():
    print('connect')


@app_socket_io.on('join')
def on_join(data):
    print(data)
    username = data['username']
    room_id_string = int(data['room_id_sting'])
    join_room(int(room_id_string))
    modify_chatroom_number(room_id_string, True)
    send(username + ' has entered the room.', to=room_id_string)


@app_socket_io.on('chat')
def broadcast(data):
    message = data['message']
    room = data['room']
    send(message, to=room)


@app_socket_io.on('leave')
def on_leave(data):
    username = data['username']
    room_id_string = int(data['room_id_string'])
    leave_room(int(room_id_string))
    modify_chatroom_number(room_id_string, True)
    send(username + ' has entered the room.', to=room_id_string)


#
#
# @app_socket_io.on('leave')
# def on_leave(data):
#     username = data['username']
#     room = data['room']
#     leave_room(room)
#     send(username + ' has left the room.', room=room)


@chatroom_bp.route('/list', methods={'GET'})
def list_room():
    res = []
    for item in chatroom_lists:
        res.append(item.getinfo())
    return str(res)


@chatroom_bp.route('/room', methods={'GET'})
def in_or_out_room():
    in_or_out = int(request.args.get('status'))
    chatroom_id_int = int(request.args.get('chatroom_id'))
    username_string = request.args.get('username')
    is_in_bool = False
    current_chatroom: Chatroom
    for i in chatroom_lists:
        if chatroom_id_int == i.id_int:
            i.people_number_int += 1
            current_chatroom = i
            is_in_bool = True
    if not is_in_bool:
        return 'chatroom id wrong'
    if in_or_out == 1:
        # on_join({'username': username_string, 'room': chatroom_id_int})
        # return 'get in chatroom:\n' + str(current_chatroom)
        return render_template('/chatroom/room.html')
    elif in_or_out == 0:
        # on_leave({'username': username_string, 'room': chatroom_id_int})
        return 'leave chatroom:\n' + str(current_chatroom)
    else:
        return 'something wrong'
