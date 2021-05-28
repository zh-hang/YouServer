import unittest
import json
import requests as re

host='http://124.70.97.253:5000/chatroom'

class TestChatroomMethods(unittest.TestCase):
    def test_test_run(self):
        print('test run successfully')

    def test_chatroom_lists(self):
        url=host+'/list'
        res=re.get(url)
        self.assertIn('room_list',res.text)
        self.assertIn('name',res.text)
        self.assertIn('population',res.text)

    def test_chatroom_join(self):
        wrong_urls=[
            '/room?name=TEST&status=0',
            '/room?name=you&status=1',
            '/room?name',
            '/room?status',
            '/room?name=YOU&status=9',
            '/room'
            ]
        for url in wrong_urls:
            r=re.get(host+url,'GET')
            if(r.status_code==200):
                self.assertIn(r.json()['res'],['invalid room','invalid status','full room'])
        right_urls=[
            '/room?name=YOU&status=1',
            '/room?name=YOU&status=0'
        ]
        for url in right_urls:
            r=re.get(host+url,'GET')
            self.assertIn(r.json()['res'],['join chatroom','leave chatroom'])


if __name__ == '__main__':
    unittest.main()