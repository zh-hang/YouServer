import unittest
import json
import requests as re

url = 'http://127.0.0.1:5000/auth'


class TestAuthUnit(unittest.TestCase):
    def test_wrong_user_tel(self):
        r = re.get(url + '/login?user_tel=1&user_password=123')
        self.assertEqual(r.json()['res'], 'user not exist')

    def test_wrong_user_password(self):
        r = re.get(url + '/login?user_tel=0&user_password=123')
        self.assertEqual(r.json()['res'], 'password wrong')

    def test_login_all_right(self):
        r = re.get(url + '/login?user_tel=0&user_password=123456')
        self.assertEqual(r.json()['res'], 'login successfully')
