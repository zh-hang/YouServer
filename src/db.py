import sqlite3
import click
from . import user as u
from flask import current_app, g
from flask.cli import with_appcontext


# 得到一个数据库连接
# 返回一个数据库的连接
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


# 关闭一个数据库连接
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# 查询数据库中是否有该用户
def search_user_by_tel(user_tel_int):
    with sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
    ) as db:
        conn = db.cursor()
        user = conn.execute(
            'SELECT * FROM user where user_tel=' + str(user_tel_int)).fetchall()
        if user is None or len(user) == 0:
            return u.User()
        return u.User(user[0][0], user[0][1], user[0][2], user[0][3])


# 查询数据库中是否有该用户
def search_user_by_name(user_name_str):
    with sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
    ) as db:
        conn = db.cursor()
        user = conn.execute(
            'SELECT * FROM user where user_name=' + "'" + user_name_str + "'").fetchall()
        if user is None or len(user) == 0:
            return u.User()
        return u.User(user[0][0], user[0][1], user[0][2], user[0][3])


def insert_user(user_tel_int, user_name_str, user_password_str):
    with sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
    ) as db:
        conn = db.cursor()
        conn.execute(
            '''INSERT INTO user (user_tel,user_name,user_password,user_avatar_url) VALUES (?,?,?,?)''',
            (user_tel_int, user_name_str, user_password_str,'default')
        )
