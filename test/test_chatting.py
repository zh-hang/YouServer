import asyncio
from asyncio.tasks import sleep
import websockets
import threading
import json
import unittest
import requests

package = {
    "type": "",
    "data": {
        "user": {
            "user_name": "",
            "user_avatar": ""
        },
        "room_name": "",
        "msg": ""
    }
}

uri = "ws://localhost:2333"


async def test_join():
    async with websockets.connect(uri) as websocket:
        package['type'] = 'join'
        package['data']['user']['user_name'] = 'test'
        package['data']['room_name'] = 'YOU'
        await websocket.send(json.dumps(package))
        res_msg = await websocket.recv()
        print(json.loads(res_msg)['data']['msg'])
        assert ('join' == json.loads(res_msg)['data']['msg'])
        print(json.loads(res_msg))


async def get_join_return_message(user_name='', room_name='', msg=''):
    package['type'] = 'join'
    package['data']['user']['user_name'] = user_name
    package['data']['room_name'] = room_name
    package['data']['msg'] = msg
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(package))
        res_msg = await websocket.recv()
        r = requests.get('http://127.0.0.1:5000/chatroom/list')
        print(r.json())
        return json.loads(res_msg)


async def get_check_return_message(data_type=None, user_name=None, room_name=None, msg=''):
    if data_type is None:
        package.pop('type')
    else:
        package['type'] = data_type
    if user_name is None and room_name is None:
        package.pop('data')
    else:
        package['data']['user']['user_name'] = user_name
        package['data']['room_name'] = room_name
        package['data']['msg'] = msg
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(package))
        res_msg = await websocket.recv()
        return json.loads(res_msg)


async def get_leave_return_message(user_name='', room_name='', msg=''):
    package['data']['user']['user_name'] = user_name
    package['data']['room_name'] = room_name
    package['data']['msg'] = msg
    async with websockets.connect(uri) as websocket:
        package['type'] = 'join'
        await websocket.send(json.dumps(package))
        await websocket.recv()
        package['type'] = 'leave'
        await sleep(0.5)
        await websocket.send(json.dumps(package))
        res_msg = await websocket.recv()
        return json.loads(res_msg)


def set_package(data_type=None, user_name=None, room_name=None, msg=None):
    temp_package = package
    if data_type is not None:
        temp_package['type'] = data_type
    if user_name is not None:
        temp_package['data']['user']['user_name'] = user_name
    if room_name is not None:
        temp_package['data']['room_name'] = room_name
    if msg is not None:
        temp_package['data']['msg'] = msg
    return temp_package


break_timer = False


def loop_break():
    global break_timer
    break_timer = True


async def run_client(curr_package):
    async with websockets.connect(uri) as websocket:
        curr_package['type'] = 'join'
        await websocket.send(json.dumps(curr_package))
        await websocket.recv()
        curr_package['type'] = 'msg'
        while True and not break_timer:
            msg = await websocket.recv()
            await sleep(1)
            await websocket.send(json.dumps(curr_package))
            yield msg


class TestChattingUnit(unittest.TestCase):
    def test_test_case_available(self):
        self.assertTrue('test run success')

    async def join_with_right_data(self):
        new_msg = await get_join_return_message('test', 'TEST')
        self.assertEqual(new_msg['data']['msg'], 'create')
        await sleep(1)
        new_msg = await get_join_return_message('test', 'TEST')
        self.assertEqual(new_msg['data']['msg'], 'join')
        r = requests.get('http://127.0.0.1:5000/chatroom/list')
        for room in r.json()['room_list']:
            if room['name'] == 'TEST':
                self.assertEqual(0, room['population'])

    def test_join_with_right_data(self):
        loop = asyncio.events.new_event_loop()
        asyncio.events.set_event_loop(loop)
        loop.run_until_complete(self.join_with_right_data())

    async def data_check(self, data_type='', user_name='', room_name=''):
        if user_name == '' and room_name == '':
            new_msg = await get_check_return_message(data_type=data_type)
            self.assertEqual(new_msg['data']['msg'], 'invalid data')
        else:
            new_msg = await get_check_return_message(data_type=data_type, user_name=user_name, room_name=room_name)
            if data_type == '':
                self.assertEqual(new_msg['data']['msg'], 'illegal type')
            elif user_name == '' or room_name == '':
                self.assertEqual(new_msg['data']['msg'], 'illegal data')

    def test_data_check(self):
        data_type = 'join'
        user_name = 'test'
        room_name = 'YOU'
        loop = asyncio.events.new_event_loop()
        asyncio.events.set_event_loop(loop)
        loop.run_until_complete(self.data_check(user_name=user_name, room_name=room_name))
        loop.run_until_complete(self.data_check(data_type=data_type, room_name=room_name))
        loop.run_until_complete(self.data_check(data_type=data_type, user_name=user_name))

    async def leave_with_right_data(self):
        new_msg = await get_leave_return_message('test', 'TEST')
        self.assertEqual(new_msg['data']['msg'], 'leave')

    def test_leave_with_right_data(self):
        loop = asyncio.events.new_event_loop()
        asyncio.events.set_event_loop(loop)
        loop.run_until_complete(self.leave_with_right_data())

    async def send_msg_with_right_data(self, user_name):
        curr_package = set_package(data_type='join', user_name=user_name, room_name='TEST')
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps(curr_package))
            await websocket.recv()
            curr_package = set_package(data_type='msg', user_name=user_name, room_name='TEST', msg=user_name)
            while not break_timer:
                await websocket.send(json.dumps(curr_package))
                new_msg = await websocket.recv()
                self.assertIn(json.loads(new_msg)['data']['msg'], user_name + 'join' + 'leave' + 'create')
                await sleep(0.5)

    async def recv_msg(self, user_name, send_user_name):
        curr_package = set_package(data_type='join', user_name=user_name, room_name='TEST')
        async with websockets.connect(uri)as websocket:
            await websocket.send(json.dumps(curr_package))
            while not break_timer:
                new_msg = await websocket.recv()
                self.assertIn(json.loads(new_msg)['data']['msg'], send_user_name + 'join' + 'leave' + 'create')

    def run_recv_msg(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        asyncio.get_event_loop().run_until_complete(self.recv_msg('test2', 'test1'))

    def run_send_msg(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        asyncio.get_event_loop().run_until_complete(self.send_msg_with_right_data('test1'))

    def test_msg(self):
        timer = threading.Timer(5, loop_break)
        timer.start()
        s = threading.Thread(target=self.run_send_msg)
        r = threading.Thread(target=self.run_recv_msg)
        r.start()
        s.start()


if __name__ == '__main__':
    unittest.main()
