import functools
import json

from . import db
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import (check_password_hash, generate_password_hash)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods={'GET'})
def register():
    user_tel = request.args['user_tel']
    user_password = str(request.args['user_password'])
    user_name = str(request.args['user_name'])
    user = db.search_user_by_tel(int(user_tel))
    if user.not_init():
        db.insert_user(user_tel, user_name, user_password)
        return json.dumps({'res': 'register successfully'})
    return json.dumps({'res': 'user exist'})


@auth_bp.route('/login', methods={'GET'})
def login():
    user_tel = request.args['user_tel']
    user_password = str(request.args['user_password'])
    user = db.search_user_by_tel(int(user_tel))
    if user.not_init():
        return json.dumps({'res': 'user not exist', 'data': {}})
    if user.is_password_right(user_password):
        return json.dumps({'res': 'login successfully', 'data': user.get_dict()})
    else:
        return json.dumps({'res': 'password wrong', 'data': {}})


@auth_bp.route('/user_data', methods={'GET'})
def user_data():
    user = None
    if 'user_name' in request.args.keys():
        user_name = str(request.args['user_name'])
        user = db.search_user_by_name(user_name)
    if 'user_tel' in request.args.keys():
        user_tel = int(request.args['user_tel'])
        user = db.search_user_by_tel(user_tel)
    if user is None or user.not_init():
        return json.dumps({'res': 'user not exist', 'data': {}})
    return json.dumps({'res': 'get user data successfully', 'data': {'user': user.get_dict()}})
