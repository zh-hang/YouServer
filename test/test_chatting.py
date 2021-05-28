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


uri="ws://localhost:2333"

async def test_join():
    async with websockets.connect(uri) as websocket:
        package['type']='join'
        package['data']['user_name']='test'
        package['data']['room_name']='YOU'
        await websocket.send(json.dumps(package))
        res_msg = await websocket.recv()
        print(json.loads(res_msg)['data']['msg'])
        assert('join'==json.loads(res_msg)['data']['msg'])
        print(json.loads(res_msg))


class TestChattingUnit(unittest.TestCase):
    # def test_test_case_available(self):
    #     self.assertFalse('test run success')

    async def get_return_message(self,data_type='',user_name='',room_name='',msg=''):
        package['type']=data_type
        package['data']['name']=user_name
        package['data']['room_name']=room_name
        package['data']['msg']=msg
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps(package))
            res_msg = await websocket.recv()
            return json.loads(res_msg)

    async def join_with_right_data(self):
        new_msg= await self.get_return_message('join','test','TEST')
        self.assertIn(new_msg['data']['msg'],'create')
        new_msg= await self.get_return_message('join','test2','TEST')
        self.assertIn(new_msg['data']['msg'],'join')

    
    def test_join_with_right_data(self):
        loop = asyncio.events.new_event_loop()
        asyncio.events.set_event_loop(loop)
        loop.run_until_complete(self.join_with_right_data())

    async def join_with_wrong_data(self,data_type='',user_name='',room_name=''):
        new_msg=await self.get_return_message(data_type,user_name,room_name)
        self.assertIn(new_msg['data']['msg'],'invalid message'+'invalid msg'+'invalid data'+'illegal type'+'inllegal data')

    def test_join_with_wrong_data(self):
        data_type='join'
        user_name='test'
        room_name='YOU'
        loop = asyncio.events.new_event_loop()
        asyncio.events.set_event_loop(loop)
        loop.run_until_complete(self.join_with_wrong_data(user_name=user_name,room_name=room_name))
        loop.run_until_complete(self.join_with_wrong_data(data_type=data_type,room_name=room_name))
        loop.run_until_complete(self.join_with_wrong_data(data_type=data_type,user_name=user_name))

if __name__=='__main__':
    unittest.main()