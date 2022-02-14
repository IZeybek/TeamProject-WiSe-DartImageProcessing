import json
import pprint
import websockets
import threading
import asyncio

async def send():
    async with websockets.connect("ws://127.0.0.1:9000") as sock:
        while True:
            json1 = json.dumps({"request": int(10)})
            print("Send Message: " + str(json1))
            await sock.send(json1)
            await asyncio.sleep(3)
            json2 = json.dumps({"request": int(404)})
            print("Send Message: " + str(json2))
            await sock.send(json2)
            await asyncio.sleep(3)
            #msg = await sock.recv()
            #print("New Message: " + str(msg))
            await asyncio.sleep(3)

async def listen():
    async with websockets.connect("ws://127.0.0.1:9000") as sock:
        while True:
            json1 = json.dumps({"request": int(404)})
            print("Send Message: " + str(json1))
            await sock.send(json1)
            msg = await sock.recv()
            print("New Message: " + str(msg))

if "__main__" == __name__:
    #asyncio.get_event_loop().run_until_complete(send())
    asyncio.get_event_loop().run_until_complete(listen())
