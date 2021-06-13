import sqlite3


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

    def empty(self):
        if self.population_int == 0:
            return True
        return False

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
