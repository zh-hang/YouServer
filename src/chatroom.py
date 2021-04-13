import sqlite3

from . import db
from flask_socketio import SocketIO, emit
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

    def __str__(self):
        return 'id:' + str(self.id_int) + ' name:' + self.name_string + ' people_number:' + str(self.people_number_int)


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


@chatroom_bp.route('/list', methods={'GET'})
def list_room():
    res = []
    for item in chatroom_lists:
        res.append(item.getinfo())
    return str(res)


@chatroom_bp.route('/room', methods={'GET'})
def get_in_room():
    chatroom_id_int = int(request.args.get('chatroom_id'))
    is_in_bool = False
    current_chatroom: Chatroom
    for i in chatroom_lists:
        if chatroom_id_int == i.id_int:
            i.people_number_int += 1
            current_chatroom = i
            is_in_bool = True
    if not is_in_bool:
        return 'chatroom id wrong'
    return 'get in chatroom ' + current_chatroom.name_string
