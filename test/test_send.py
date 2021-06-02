import asyncio
import json
import websockets
import test_chatting as tc


async def hello():
    uri = "ws://124.70.97.253:2333"
    async with websockets.connect(uri) as websocket:
        package = tc.set_package('join', 'test', 'TEST')
        await websocket.send(json.dumps(package))
        await websocket.recv()
        for i in range(5):
            package = tc.set_package('msg', 'test', 'TEST', str(i))
            await websocket.send(json.dumps(package))
            greeting = await websocket.recv()
            print(f"< {json.loads(greeting)}")


asyncio.get_event_loop().run_until_complete(hello())
