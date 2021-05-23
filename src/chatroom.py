import sqlite3
import json

from . import db,chatting
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app)
from werkzeug.security import (check_password_hash, generate_password_hash)

chatroom_bp = Blueprint('chatroom', __name__, url_prefix='/chatroom')


class Chatroom:
    def __init__(self, chatroom_id_int, chatroom_name_string):
        self.id_int = chatroom_id_int
        self.name_string = chatroom_name_string
        self.population_int = 0

    def getinfo(self):
        return {'id': self.id_int, 'name': self.name_string, 'population': self.population_int}

    def __eq__(self, other_chatroom):
        return self.id_int == other_chatroom.id_int

    def __str__(self):
        return '{"id":' + str(self.id_int) + ',"name":' + self.name_string + ',"population":' + str(
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


def modify_chatroom_number(chatroom_id_int, is_in_bool):
    for i in chatroom_lists:
        if i.id_int == chatroom_id_int:
            if is_in_bool:
                i.population_int += 1
            else:
                i.population_int -= 1



@chatroom_bp.route('/list', methods={'GET'})
def list_room():
    res = []
    for item in chatroom_lists:
        res.append(item.getinfo())
    return str({'room_list':res})

@chatroom_bp.route('/connect_test',methods={'GET'})
def connect_test():
    return 'connect successfully'