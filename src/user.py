class User:
    def __init__(self, user_tel_int=-1, user_name_str='', user_password_str='', user_avatar_url_str=''):
        self.user_tel = user_tel_int
        self.user_name = user_name_str
        self.user_password = user_password_str
        self.user_avatar_url = user_avatar_url_str

    def is_password_right(self, password_str):
        if self.user_password == password_str:
            return True
        return False

    def not_init(self):
        if self.user_tel == -1:
            return True
        return False

    def get_dict(self):
        return {'user_tel': self.user_tel, 'user_name': self.user_name, 'user_password': self.user_password,
                'user_avatar_url': self.user_avatar_url}
