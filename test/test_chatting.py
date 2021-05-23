import asyncio
from asyncio.tasks import sleep
import websockets

async def hello():
    uri = "ws://localhost:2333"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

for i in range(10):
    asyncio.get_event_loop().run_until_complete(hello())
    sleep(1000)