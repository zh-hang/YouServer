import unittest
import json
import requests as re

host = 'http://127.0.0.1:5000/chatroom'


def get_res(url, method=None):
    r = re.get(url, method)
    if r.status_code == 200:
        return r.json()


def get_room_url(room_name_str, user_name_str, status_str):
    return host + '/room?room_name=' + room_name_str + '&user_name=' + user_name_str + '&status=' + status_str


class TestChatroomMethods(unittest.TestCase):
    def test_test_run(self):
        print('test run successfully')

    def test_chatroom_lists(self):
        url = host + '/list'
        res = re.get(url)
        self.assertIn('room_list', res.text)
        self.assertIn('name', res.text)
        self.assertIn('population', res.text)

    def test_chatroom_room(self):
        url = get_room_url('NONE_TEST', 'test', '1')
        self.assertEqual(get_res(url, 'GET')['res'], 'invalid room')

        url = get_room_url('TEST', 'test', '0')
        self.assertEqual(get_res(url, 'GET')['res'], 'user not exist')

        url = get_room_url('TEST', 'test', '3')
        self.assertEqual(get_res(url, 'GET')['res'], 'invalid status')

        url = get_room_url('TEST', 'test', '1')
        for i in range(10):
            get_res(url, 'GET')
        self.assertEqual(get_res(url, 'GET')['res'], 'full room')

        url = get_room_url('TEST', 'test', '0')
        for i in range(10):
            get_res(url, 'GET')


if __name__ == '__main__':
    unittest.main()
