import asyncio
from asyncio.tasks import sleep
import websockets
import threading
import json
import unittest

async def hello():
    uri = "ws://localhost:2333"
    async with websockets.connect(uri) as websocket:
        msg={"name":"test","msg":"test"}
        await websocket.send(json.dumps(msg))
        print(f"> {msg}")
        res_msg = await websocket.recv()
        print(json.loads(res_msg))

asyncio.get_event_loop().run_until_complete(hello())