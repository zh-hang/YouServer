#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import queue

logging.basicConfig()

ip_addr = '0.0.0.0'

MESSAGE_OK = 0
INVALID_MESSAGE = 1
INVALID_DATA = 2
ILLEGAL_DATA = 3
NULL_MSG = 4
USER_NOT_EXIST = 5
ROOM_NOT_EXIST = 6


def checkout_data(message):
    print(message)
    if 'type' not in message or 'data' not in message:
        new_message = json.dumps(message_generate(type_str='error', msg_str='invalid message'))
        return INVALID_MESSAGE, new_message

    if 'type' == '':
        new_message = json.dumps(message_generate(type_str='error', msg_str='illegal type'))
        return INVALID_MESSAGE, new_message

    data = message['data']
    if 'user' not in data or 'room_name' not in data or 'msg' not in data:
        new_message = json.dumps(message_generate(type_str='error', msg_str='invalid data'))
        return INVALID_DATA, new_message

    if data['user']['user_name'] == '' or data['room_name'] == '' \
            or data['user']['user_name'] is None or data['room_name'] is None:
        new_message = json.dumps(message_generate(type_str='error', msg_str='illegal data'))
        return ILLEGAL_DATA, new_message

    return MESSAGE_OK, ''


class ChatUser:
    def __init__(self, user_chat_user, user_avatar_str):
        self.user_name = user_chat_user
        self.user_avatar = user_avatar_str

    def get_dict(self):
        return {'user_name': self.user_name, 'user_avatar': self.user_avatar}

    def __str__(self):
        return str({'user_name': self.user_name, 'user_avatar': self.user_avatar})

    def __eq__(self, other):
        if self.user_name == other.user_name:
            return True
        return False


def message_generate(type_str='', user_chat_user=ChatUser('', ''), room_name_str='', msg_str=''):
    return {
        'type': type_str,
        'data': {
            'user': user_chat_user.get_dict(),
            'room_name': room_name_str,
            'msg': msg_str
        }
    }



class ChatRoomServer:
    def __init__(self):
        self.MSG = queue.Queue()
        self.ROOMS = dict()

    def message_event(self):
        if self.MSG.empty():
            return None
        return self.MSG.get()

    async def notify_message(self):
        msg = self.message_event()
        if msg is not None and self.ROOMS.keys():
            await asyncio.wait(
                [user['socket'].send(json.dumps(msg)) for user in self.ROOMS[msg['data']['room_name']]])

    async def register(self, websocket, room_name_str, user_chat_user):
        if room_name_str in self.ROOMS.keys():
            self.ROOMS[room_name_str].append(
                {'user': user_chat_user, 'socket': websocket})
            message = json.dumps(message_generate(type_str='user', user_chat_user=user_chat_user, msg_str='join'))
            await asyncio.wait([user['socket'].send(message) for user in self.ROOMS[room_name_str]])
        else:
            self.ROOMS[room_name_str] = [
                {'user': user_chat_user, 'socket': websocket}]
            message = json.dumps(message_generate(type_str='user', user_chat_user=user_chat_user, msg_str='create'))
            await asyncio.wait([user['socket'].send(message) for user in self.ROOMS[room_name_str]])

    async def unregister(self, room_name_str, user_chat_user=None):
        message = message_generate(type_str='user', user_chat_user=user_chat_user, msg_str='leave')
        if room_name_str in self.ROOMS.keys():
            for item in self.ROOMS[room_name_str]:
                if item['user'] == user_chat_user:
                    self.ROOMS[room_name_str].remove(item)
                    if len(self.ROOMS[room_name_str]) != 0:
                        await asyncio.wait(
                            [user['socket'].send(json.dumps(message)) for user in self.ROOMS[room_name_str]])
                    return MESSAGE_OK, ''
                message['data']['msg'] = 'user not exist'
                return USER_NOT_EXIST, json.dumps(message)
        message['data']['msg'] = 'room not exist'
        return ROOM_NOT_EXIST, json.dumps(message)

    async def counter(self, websocket, path):
        data = dict()
        is_join = False
        try:
            async for message in websocket:
                data = json.loads(message)
                checkout_res = checkout_data(data)
                if checkout_res[0] != MESSAGE_OK:
                    await websocket.send(checkout_res[1])
                    continue
                user = ChatUser(data['data']['user']['user_name'], data['data']['user']['user_avatar'])
                if data['type'] == 'join':
                    is_join = True
                    await self.register(websocket, data['data']['room_name'], user)
                    continue

                elif data['type'] == 'leave':
                    leave_res = await self.unregister(data['data']['room_name'], user)
                    if leave_res[0] != MESSAGE_OK:
                        await websocket.send(leave_res[1])
                    continue

                elif data['type'] == 'msg':
                    if 'msg' in data['data']:
                        if data['data']['msg'] != '':
                            self.MSG.put(
                                data, block=True, timeout=1000)
                            await self.notify_message()
                            continue
                        else:
                            message = json.dumps(message_generate(type_str='error', msg_str='null message'))
                    else:
                        message = json.dumps(message_generate(type_str='error', msg_str='invalid msg'))
                else:
                    message = json.dumps(message_generate(type_str='error', msg_str='illegal type'))
                await websocket.send(message)

        finally:
            if is_join:
                await self.unregister(data['data']['room_name'],
                                      ChatUser(data['data']['user']['user_name'], data['data']['user']['user_avatar']))

    def run(self):
        global ip_addr
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        start_server = websockets.serve(self.counter, ip_addr, 2333)
        print('webserver run')
        asyncio.get_event_loop().run_until_complete(start_server)

        asyncio.get_event_loop().run_forever()

    def close(self):
        asyncio.get_event_loop().close()


if __name__ == '__main__':
    server = ChatRoomServer()
    server.run()
