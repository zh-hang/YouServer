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

        r = re.get(url + '/login?user_tel=0')
        self.assertEqual(r.json()['res'], 'missing parameters')
        r = re.get(url + '/login?user_tel=0&user_password=123456')
        self.assertEqual(r.json()['res'], 'login successfully')

    def test_register(self):
        user_tel = 23333
        user_name = 'test5'
        user_password = 123456
        curr_url = url + '/register?user_tel=' + str(user_tel)
        r = re.get(curr_url)
        self.assertEqual(r.json()['res'], 'missing parameters')
        curr_url = url + '/register?user_tel=' + str(user_tel) + '&user_name=' + user_name + '&user_password=' + str(
            user_password)
        r = re.get(curr_url)
        self.assertEqual(r.json()['res'], 'register successfully')
        r = re.get(curr_url)
        self.assertEqual(r.json()['res'], 'user exist')

    def test_get_user_data(self):
        user_tel = 0
        user_name = 'admin'
        curr_url = url + '/user_data'
        r = re.get(curr_url)
        self.assertEqual(r.json()['res'], 'user not exist')

        curr_url = url + '/user_data?user_name=asdfasdf'
        r = re.get(curr_url)
        self.assertEqual(r.json()['res'], 'user not exist')

        curr_url = url + '/user_data?user_name=' + user_name
        r = re.get(curr_url)
        self.assertEqual(r.json()['res'], 'get user data successfully')

        curr_url = url + '/user_data?user_tel=' + str(user_tel)
        r = re.get(curr_url)
        self.assertEqual(r.json()['res'], 'get user data successfully')

        curr_url = url + '/user_data?user_tel=' + str(1)
        r = re.get(curr_url)
        self.assertEqual(r.json()['res'], 'user not exist')
