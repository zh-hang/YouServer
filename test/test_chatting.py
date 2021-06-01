import asyncio
from asyncio.tasks import sleep
import websockets
import threading
import json
import unittest

package = {
    "type": "",
    "data": {
        "user_name": "",
        "room_name": "",
        "msg": "",
    }
}

uri = "ws://localhost:2333"


async def test_join():
    async with websockets.connect(uri) as websocket:
        package['type'] = 'join'
        package['data']['user_name'] = 'test'
        package['data']['room_name'] = 'YOU'
        await websocket.send(json.dumps(package))
        res_msg = await websocket.recv()
        print(json.loads(res_msg)['data']['msg'])
        assert ('join' == json.loads(res_msg)['data']['msg'])
        print(json.loads(res_msg))


async def get_join_return_message(user_name='', room_name='', msg=''):
    package['type'] = 'join'
    package['data']['user_name'] = user_name
    package['data']['room_name'] = room_name
    package['data']['msg'] = msg
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(package))
        res_msg = await websocket.recv()
        return json.loads(res_msg)


async def get_check_return_message(data_type=None, user_name=None, room_name=None, msg=''):
    if data_type is None:
        package.pop('type')
    else:
        package['type'] = data_type
    if user_name is None and room_name is None:
        package.pop('data')
    else:
        package['data']['user_name'] = user_name
        package['data']['room_name'] = room_name
        package['data']['msg'] = msg
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(package))
        res_msg = await websocket.recv()
        return json.loads(res_msg)


async def get_leave_return_message(user_name='', room_name='', msg=''):
    package['data']['user_name'] = user_name
    package['data']['room_name'] = room_name
    package['data']['msg'] = msg
    async with websockets.connect(uri) as websocket:
        package['type'] = 'join'
        await websocket.send(json.dumps(package))
        await websocket.recv()
        package['type'] = 'leave'
        await websocket.send(json.dumps(package))
        res_msg = await websocket.recv()
        return json.loads(res_msg)


class TestChattingUnit(unittest.TestCase):
    def test_test_case_available(self):
        self.assertFalse('test run success')

    async def join_with_right_data(self):
        new_msg = await get_join_return_message('test', 'TEST')
        self.assertEqual(new_msg['data']['msg'], 'create')
        await sleep(1)
        new_msg = await get_join_return_message('test', 'TEST')
        self.assertEqual(new_msg['data']['msg'], 'join')

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
        self.assertEqual(new_msg['data']['msg'], 'join')

    def test_leave_with_right_data(self):
        loop = asyncio.events.new_event_loop()
        asyncio.events.set_event_loop(loop)
        loop.run_until_complete(self.leave_with_right_data())


if __name__ == '__main__':
    unittest.main()
