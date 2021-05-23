#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import queue

logging.basicConfig()


class Message:
    def __init__(self,user_name_str,message_str):
        msg={"name":user_name_str,"msg":message_str}
    
    def __str__(self) -> str:
        return str(self.msg)


class ChatRoomServer:
    MSG = queue.Queue()
    USERS = set()

    def __init__(self, chatroom_name_str):
        NAME = chatroom_name_str

    def users_event(self):
        return json.dumps({"type": "users", "count": len(self.USERS)})

    async def notify_message(self):
        while True:
            if not self.MSG.empty():
                msg=self.MSG.get()
                if self.USERS:
                    await asyncio.wait([user.send(msg) for user in self.USERS])

    async def notify_users(self):
        if self.USERS:
            message = self.users_event()
            await asyncio.wait([user.send(message) for user in self.USERS])

    async def register(self, websocket):
        self.USERS.add(websocket)
        await self.notify_users()

    async def unregister(self, websocket):
        self.USERS.remove(websocket)
        await self.notify_users()

    async def counter(self, websocket, path):
        await self.register(websocket)
        try:
            # await websocket.send(self.state_event())
            async for message in websocket:
                data = json.loads(message)
                if data["name"]is not None and data["msg"] is not None:
                    await self.MSG.put(Message(data["name"],data["msg"]),block=True,timeout=1000)
                else:
                    logging.error("unsupported event: %s", data)
        finally:
            await self.unregister(websocket)

    def run(self):
        start_server = websockets.serve(self.counter, "localhost", 2333)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

if __name__=="__main__":
    server=ChatRoomServer('test')
    server.run()