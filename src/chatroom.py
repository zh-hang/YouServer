import sqlite3
import json
import threading

from . import db, chatting
from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for, current_app)
from werkzeug.security import (check_password_hash, generate_password_hash)

chatroom_bp = Blueprint('chatroom', __name__, url_prefix='/chatroom')


class Chatroom:
    def __init__(self, chatroom_id_int, chatroom_name_str):
        self.id_int = chatroom_id_int
        self.name_str = chatroom_name_str
        self.population_int = 0

    def get_dict(self):
        return {'name': self.name_str, 'population': self.population_int}

    def __eq__(self, other_chatroom):
        return self.id_int == other_chatroom.id_int

    def __str__(self):
        return '{"name":' + self.name_str + ',"population":' + str(
            self.population_int) + '}'


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

new_chatting = chatting.ChatRoomServer()

thread = threading.Thread(target=new_chatting.run)
thread.start()


MODIFY_JOIN=0
MODIFY_LEAVE=1
MODIFY_INVALID_STATUS=2
MODIFY_INVALID_ROOM=3
MODIFY_FULL_ROOM=4
def modify_chatroom_population(chatroom_name_str, in_or_out):
    for i in chatroom_lists:
        if i.name_str == chatroom_name_str:
            if in_or_out==1:
                if i.population_int >=10:
                    return MODIFY_FULL_ROOM
                i.population_int += 1
                return MODIFY_JOIN
            elif in_or_out==0:
                i.population_int -= 1
                return MODIFY_LEAVE
            return MODIFY_INVALID_STATUS
    return MODIFY_INVALID_ROOM

@chatroom_bp.route('/')
def hello():
    return 'hello'

@chatroom_bp.route('/list', methods={'GET'})
def list_room():
    res = []
    for item in chatroom_lists:
        res.append(item.get_dict())
    return json.dumps({'room_list': res})




@chatroom_bp.route('/room', methods={'GET'})
def in_or_out_room():
    in_or_out = int(request.args.get('status'))
    chatroom_name = str(request.args.get('name'))
    is_modified = modify_chatroom_population(chatroom_name, in_or_out)
    if is_modified==MODIFY_JOIN:
        return json.dumps({'res':'join chatroom'})
    elif is_modified==MODIFY_LEAVE:
        return json.dumps({'res':'leave chatroom'})
    elif is_modified==MODIFY_INVALID_STATUS:
        return json.dumps({'res':'invalid status'})
    elif is_modified==MODIFY_INVALID_ROOM:
        return json.dumps({'res':'invalid room'})
    elif is_modified==MODIFY_FULL_ROOM:
        return json.dumps({'res':'room full'})

