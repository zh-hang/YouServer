import functools
import json

from . import db
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import (check_password_hash, generate_password_hash)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods={'GET'})
def login():
    user_tel = request.args['user_tel']
    user_password = str(request.args['user_password'])
    user = db.search_user(int(user_tel))
    if user.not_init():
        return json.dumps({'res': 'user not exist', 'data': {}})
    if user.is_password_right(user_password):
        return json.dumps({'res': 'login successfully', 'data': user.get_dict()})
    else:
        return json.dumps({'res': 'password wrong', 'data': {}})
