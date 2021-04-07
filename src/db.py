import sqlite3

import click
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
