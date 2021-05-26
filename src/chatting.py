#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import queue
import threading

logging.basicConfig()


class ChatRoomServer:
    def __init__(self):
        self.MSG = queue.Queue()
        self.ROOMS = dict()

    def checkout_data(self, websocket, data):
        if data['type'] == None or data['data'] == None or data['data']['user_name'] == None:
            websocket.send({'type': 'error', 'data': {
                           'user_name': data['data']['user_name'], 'room_name': '', 'msg': 'invalid data'}})
            return False
        return True

    def message_event(self):
        if self.MSG.empty():
            return None
        msg = self.MSG.get()
        return json.dumps({'type': 'msg', 'data': msg})

    async def notify_message(self):
        msg = self.message_event()
        if msg != None and self.ROOMS:
            await asyncio.wait([user.send(msg) for user in self.ROOMS[msg['room_name']]])

    async def register(self, websocket, room_name_str, user_name_str):
        if room_name_str == None or user_name_str == None:
            websocket.send({'type': 'error', 'data': {
                           'user_name': user_name_str, 'room_name': room_name_str, 'msg': 'invalid data'}})

        if room_name_str in self.ROOMS:
            self.ROOMS[room_name_str].append(
                {'user': user_name_str, 'socket': websocket})
            message = {'type': 'user', 'data': {
                'user_name': user_name_str, 'room_name': room_name_str, 'msg': 'join'}}
            await asyncio.wait([user['socket'].send(message) for user in self.ROOMS[room_name_str]])

        else:
            self.ROOMS[room_name_str] = [websocket]
            message = {'type': 'user', 'data': {
                'user_name': user_name_str, 'room_name': room_name_str, 'msg': 'create'}}
            await asyncio.wait([user['socket'].send(message) for user in self.ROOMS[room_name_str]])

    async def unregister(self, websocket, room_name_str, user_name_str):
        if room_name_str in self.ROOMS:
            for item in self.ROOMS[room_name_str]:
                if item['user'] == user_name_str:
                    self.ROOMS[room_name_str].remove(item)
                    message = {'type': 'user', 'data': {
                        'user_name': user_name_str, 'room_name': room_name_str, 'msg': 'leave'}}
                    await asyncio.wait([user['socket'].send(message) for user in self.ROOMS[room_name_str]])

        websocket.close()

    async def counter(self, websocket, path):
        try:
            async for message in websocket:
                if not self.checkout_data(message):
                    continue

                data = json.loads(message)

                if data['type'] == 'join':
                    await self.register(websocket, data['data']['room_name'], data['data']['user_name'])

                elif data['type'] == 'leave':
                    await self.unregister(websocket, data['data']['room_name'], data['data']['user_name'])

                elif data['type'] == 'msg':
                    if data['data']['msg'] is not None:
                        self.MSG.put(data['data'], block=True, timeout=1000)
                        await self.notify_message()
                    else:
                        logging.error('unsupported event: %s', data)

        finally:
            await self.unregister(websocket)

    def run(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        start_server = websockets.serve(self.counter, 'localhost', 2333)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    def close(self):
        asyncio.get_event_loop().close()


class ChattingPool:
    def __init__(self) -> None:
        self.server_pool = set()
        self.server_name_lists = list()

    def create_server(self, chatroom_name_str):
        is_in = False
        for server in self.server_name_lists:
            if(chatroom_name_str == server.NAME):
                is_in = True
        if is_in:
            self.server_pool.add(ChatRoomServer(chatroom_name_str))


if __name__ == '__main__':
    server = ChatRoomServer()
    server.run()
