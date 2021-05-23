import os

from flask import Flask, redirect, url_for



# 创建一个flask实例
# 设置缺省配置，SECRET_KEY应该是一个随机数
# 如果config.py存在这设置其中的配置
# 注册蓝图

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'you.db'),
    )
    print(app.config['DATABASE'])
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    global app_socket_io

    # @app_socket_io.on('message')
    # def handle_message(message):
    #     print('received message:' + message)
    #     send('got it')
    #
    # @app_socket_io.on('join')
    # def on_join(data):
    #     username = data['username']
    #     room = data['room']
    #     join_room(room)
    #     send(username + ' has entered the room.', room=room)
    #
    # @app_socket_io.on('leave')
    # def on_leave(data):
    #     username = data['username']
    #     room = data['room']
    #     leave_room(room)
    #     send(username + ' has left the room.', room=room)

    from . import auth, chatroom, db

    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(chatroom.chatroom_bp)

    @app.route('/')
    def init():
        return 'hello world'


    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
