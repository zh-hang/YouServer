#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import queue
import threading

logging.basicConfig()


INVALID_MSG = 0
INVALID_DATA = 1
ILLEGAL_DATA = 3


class ChatRoomServer:
    def __init__(self):
        self.MSG = queue.Queue()
        self.ROOMS = dict()

    def checkout_data(self,  message):
        if 'type'not in message or 'data' not in message:
            new_message = json.dumps({'type': 'error', 'data': {
                                     'user_name': '', 'room_name': '', 'msg': 'invalid message'}})
            return (INVALID_MSG, new_message)
        data = message['data']
        if 'user_name'not in data or 'room_name'not in data or 'msg'not in data:
            new_message = json.dumps({'type': 'error', 'data': {
                                     'user_name': '', 'room_name': '', 'msg': 'invalid data'}})
            return (INVALID_DATA, new_message)
        if data['user_name'] == '' or data['room_name'] == '':
            new_message = json.dumps({'type': 'error', 'data': {
                                     'user_name': '', 'room_name': '', 'msg': 'illegal data'}})
            return (INVALID_DATA, new_message)
        return (True, '')

    def message_event(self):
        if self.MSG.empty():
            return None
        msg = self.MSG.get()
        return json.dumps({'type': 'msg', 'data': msg})

    async def notify_message(self):
        msg = self.message_event()
        if msg != None and self.ROOMS.keys():
            await asyncio.wait([user.send(msg) for user in self.ROOMS[msg['room_name']]])

    async def register(self, websocket, room_name_str, user_name_str):
        if room_name_str == None or user_name_str == None:
            message = json.dumps({'type': 'error', 'data': {
                                 'user_name': user_name_str, 'room_name': room_name_str, 'msg': 'invalid data'}})
            await asyncio.wait(websocket.send(message))

        if room_name_str in self.ROOMS.keys():
            self.ROOMS[room_name_str].append(
                {'user': user_name_str, 'socket': websocket})
            message = json.dumps({'type': 'user', 'data': {
                                 'user_name': user_name_str, 'room_name': room_name_str, 'msg': 'join'}})
            await asyncio.wait([user['socket'].send(message) for user in self.ROOMS[room_name_str]])

        else:
            self.ROOMS[room_name_str] = [
                {'user': user_name_str, 'socket': websocket}]
            message = json.dumps({'type': 'user', 'data': {
                                 'user_name': user_name_str, 'room_name': room_name_str, 'msg': 'create'}})
            await asyncio.wait([user['socket'].send(message) for user in self.ROOMS[room_name_str]])

    async def unregister(self, room_name_str, user_name_str):
        if room_name_str in self.ROOMS.keys():
            print(self.ROOMS)
            for item in self.ROOMS[room_name_str]:
                if item['user'] == user_name_str:
                    self.ROOMS[room_name_str].remove(item)
                    message = {'type': 'user', 'data': {
                        'user_name': user_name_str, 'room_name': room_name_str, 'msg': 'leave'}}
                    if len(self.ROOMS[room_name_str]) != 0:
                        await asyncio.wait([user['socket'].send(json.dumps(message)) for user in self.ROOMS[room_name_str]])

        # websocket.close()

    async def counter(self, websocket, path):
        is_join = False
        try:
            async for message in websocket:
                data = json.loads(message)
                checkout_res = self.checkout_data(data)
                if not checkout_res[0]:
                    await websocket.send(checkout_res[1])
                    continue
                is_join = True
                if data['type'] == 'join':
                    await self.register(websocket, data['data']['room_name'], data['data']['user_name'])
                    continue

                elif data['type'] == 'leave':
                    await self.unregister(data['data']['room_name'], data['data']['user_name'])
                    continue

                elif data['type'] == 'msg':
                    if 'msg' in data['data']:
                        if data['data']['msg'] != '':
                            self.MSG.put(
                                data['data'], block=True, timeout=1000)
                            await self.notify_message()
                            continue
                        else:
                            message = json.dumps({'type': 'error', 'data': {
                                                 'user_name': '', 'room_name': '', 'msg': 'null message'}})
                    else:
                        message = json.dumps({'type': 'error', 'data': {
                                             'user_name': '', 'room_name': '', 'msg': 'invalid msg'}})
                else:
                    message = json.dumps({'type': 'error', 'data': {
                                         'user_name': '', 'room_name': '', 'msg': 'illegal type'}})
                await websocket.send(message)

        finally:
            if is_join:
                await self.unregister(data['data']['room_name'], data['data']['user_name'])

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
