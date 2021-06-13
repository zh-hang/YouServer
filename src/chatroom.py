import json
import threading

from . import db, chatting,resource
from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for, current_app)
from werkzeug.security import (check_password_hash, generate_password_hash)

chatroom_bp = Blueprint('chatroom', __name__, url_prefix='/chatroom')

try:
    with resource.ChatroomResource() as r:
        resource.chatroom_dict = r.getChatroomDict()
except Exception as e:
    print(e)

new_chatting = chatting.ChatRoomServer()

thread = threading.Thread(target=new_chatting.run)
thread.start()

@chatroom_bp.route('/')
def hello():
    return 'hello'


@chatroom_bp.route('/list', methods={'GET'})
def list_room():
    res = []
    for key in resource.chatroom_dict.keys():
        res.append(resource.chatroom_dict[key].get_dict())
    return json.dumps({'room_list': res})


@chatroom_bp.route('/create', methods={'GET'})
def create_room():
    if 'room_name' not in request.args.keys():
        return json.dumps({'res': 'missing parameters'})
    chatroom_name = str(request.args.get('room_name'))
    if chatroom_name in resource.chatroom_dict.keys():
        return json.dumps({'res': 'chatroom already exist'})
    resource.chatroom_dict[chatroom_name] = resource.Chatroom(chatroom_name)
    print('create chatroom ' + chatroom_name)
    return json.dumps({'res': 'chatroom create successfully'})
