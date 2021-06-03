import sqlite3
import json
import threading

from . import db, chatting
from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for, current_app)
from werkzeug.security import (check_password_hash, generate_password_hash)

chatroom_bp = Blueprint('chatroom', __name__, url_prefix='/chatroom')

MAX_POPULATION = 10

USER_JOIN = 0
USER_LEAVE = 1
USER_INVALID_STATUS = 2
USER_INVALID_ROOM = 3
USER_INVALID_USER = 4
USER_FULL_ROOM = 5

STATUS_LEAVE = 0
STATUS_JOIN = 1


class Chatroom:
    def __init__(self, chatroom_name_str):
        self.name_str = chatroom_name_str
        self.population_int = 0
        self.users = []

    def get_dict(self):
        return {'name': self.name_str, 'population': self.population_int}

    def add_user(self, user_name):
        if self.population_int < 10:
            self.users.append(user_name)
            self.population_int += 1
            return USER_JOIN
        return USER_FULL_ROOM

    def remove_user(self, user_name):
        for user in self.users:
            if user == user_name:
                self.users.remove(user)
                self.population_int -= 1
                return USER_LEAVE
        return USER_INVALID_USER

    def __eq__(self, other_chatroom):
        return self.name_str == other_chatroom.name_str

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
    def getChatroomDict():
        chatroom_db = sqlite3.connect('./instance/you.db')
        chatroom_db_lists = chatroom_db.execute(
            'SELECT * FROM chatroom').fetchall()
        print(chatroom_db_lists)
        chatroom_temp_dict = dict()
        for i in chatroom_db_lists:
            chatroom_temp_dict[i[1]] = Chatroom(i[1])
        chatroom_db.close()
        return chatroom_temp_dict


chatroom_dict = dict()
try:
    with ChatroomResource() as resource:
        chatroom_dict = resource.getChatroomDict()
except Exception as e:
    print(e)

new_chatting = chatting.ChatRoomServer()

thread = threading.Thread(target=new_chatting.run)
thread.start()


def user_action(chatroom_name_str, user_name_str, in_or_out):
    print(chatroom_dict)
    if chatroom_name_str in chatroom_dict.keys():
        if in_or_out == STATUS_JOIN:
            return chatroom_dict[chatroom_name_str].add_user(user_name_str)
        elif in_or_out == STATUS_LEAVE:
            return chatroom_dict[chatroom_name_str].remove_user(user_name_str)
        else:
            return USER_INVALID_STATUS
    return USER_INVALID_ROOM


@chatroom_bp.route('/')
def hello():
    return 'hello'


@chatroom_bp.route('/list', methods={'GET'})
def list_room():
    res = []
    for key in chatroom_dict.keys():
        res.append(chatroom_dict[key].get_dict())
    return json.dumps({'room_list': res})


@chatroom_bp.route('/create', methods={'GET'})
def create_room():
    chatroom_name = str(request.args.get('room_name'))
    if chatroom_name in chatroom_dict.keys():
        return json.dumps({'res': 'chatroom already exist'})
    chatroom_dict[chatroom_name] = Chatroom(chatroom_name)
    print('create chatroom ' + chatroom_name)
    return json.dumps({'res': 'chatroom create successfully'})


@chatroom_bp.route('/room', methods={'GET'})
def in_or_out_room():
    global chatroom_dict
    chatroom_name = str(request.args.get('room_name'))
    user_name = str(request.args.get('user_name'))
    in_or_out = int(request.args.get('status'))
    user_action_res = user_action(chatroom_name, user_name, in_or_out)
    if user_action_res == USER_JOIN:
        print(user_name + ' join chatroom: ' + chatroom_name)
        return json.dumps({'res': 'join chatroom'})
    elif user_action_res == USER_LEAVE:
        print(user_name + ' leave chatroom: ' + chatroom_name)
        chatroom_dict.pop(chatroom_name)
        return json.dumps({'res': 'leave chatroom'})
    elif user_action_res == USER_INVALID_STATUS:
        return json.dumps({'res': 'invalid status'})
    elif user_action_res == USER_INVALID_ROOM:
        return json.dumps({'res': 'invalid room'})
    elif user_action_res == USER_INVALID_USER:
        return json.dumps({'res': 'user not exist'})
    elif user_action_res == USER_FULL_ROOM:
        return json.dumps({'res': 'full room'})
