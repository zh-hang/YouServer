#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import queue
import threading

logging.basicConfig()

MAX_USR_NUM=20

class Message:
    def __init__(self, user_name_str, message_str):
        self.msg = {"name": user_name_str, "msg": message_str}

    def __str__(self) -> str:
        return str(self.msg)

    def get_dict(self):
        return self.msg


class ChatRoomServer:
    def __init__(self, chatroom_name_str):
        self.MSG = queue.Queue()
        self.USERS = set()

    def message_event(self):
        if self.MSG.empty():
            return None
        msg=self.MSG.get()
        return json.dumps({"type": "msg", "data": msg.get_dict()})

    def users_event(self):
        return json.dumps({"type": "users", "data": len(self.USERS)})

    async def notify_message(self):
        msg = self.message_event()
        if msg != None and self.USERS:
            await asyncio.wait([user.send(msg) for user in self.USERS])

    async def notify_users(self):
        if self.USERS:
            message = self.users_event()
            await asyncio.wait([user.send(message) for user in self.USERS])

    async def register(self, websocket):
        if(len(self.USERS)<MAX_USR_NUM):
            self.USERS.add(websocket)
            await self.notify_users()
        else:
            websocket.send(json.dumps({"type":"error","data":{"msg":"The number of people in the chatroom reaches the upper limit."}}))
            websocket.close()

    async def unregister(self, websocket):
        self.USERS.remove(websocket)
        await self.notify_users()

    async def counter(self, websocket, path):
        await self.register(websocket)
        try:
            # await websocket.send(self.state_event())
            async for message in websocket:
                data = json.loads(message)
                if "name"in data and "msg" in data and data["name"] is not None and data["msg"] is not None:
                    self.MSG.put(Message(data["name"], data["msg"]), block=True, timeout=1000)
                    await self.notify_message()
                else:
                    logging.error("unsupported event: %s", data)
        finally:
            await self.unregister(websocket)

    def run(self):
        start_server = websockets.serve(self.counter, "localhost", 2333)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    
    def close(self):
        asyncio.get_event_loop().close()
    

class ChattingPool:
    def __init__(self) -> None:
        self.server_pool=set()
        self.server_name_lists=list()
    
    def create_server(self,chatroom_name_str):
        is_in=False
        for server in self.server_name_lists:
            if(chatroom_name_str==server.NAME):
                is_in=True
        if is_in:
            self.server_pool.add(ChatRoomServer(chatroom_name_str))

if __name__ == "__main__":
    server = ChatRoomServer('test')
    server.run()
