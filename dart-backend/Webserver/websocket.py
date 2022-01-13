import asyncio
import json
import websockets
import threading

CALIBRATION_DONE = threading.Event()
ROUND_DONE = threading.Event()
IMAGE_COUNT = 0
WEBSOCKET = None
Global_LOCK = threading.Lock()
CONNECTIONS = set()

def increase_image_count():
    global IMAGE_COUNT, Global_LOCK
    Global_LOCK.acquire()
    IMAGE_COUNT = IMAGE_COUNT + 1
    Global_LOCK.release()

def reset_image_count():
    global IMAGE_COUNT, Global_LOCK, IMAGE_RESET
    Global_LOCK.acquire()
    IMAGE_COUNT = 0
    Global_LOCK.release()
    IMAGE_RESET.set()

def start_server(ip, port):
    global WEBSOCKET
    WEBSOCKET = websockets.serve(handle_requests, ip, port)
    print("Starting Server, listening on Port" + str(port))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(WEBSOCKET)
    loop.run_forever()

async def handle_requests(websocket, path):
    global CALIBRATION_DONE, CONNECTIONS
    print("A client connected!")
    try:
        async for message in websocket:
            CONNECTIONS.add(websocket)
            print("Message received from client: " + str(message))
            json_message = json.loads(message)

            if json_message["request"] == 10:
                # handle missed dart
                increase_image_count()
                print("Noticed missed Dart - Data corrected")

            elif json_message["request"] == 11:
                # handle new calibration
                CALIBRATION_DONE.clear()
                # TODO: start calibration
                CALIBRATION_DONE.wait()
                json_response = json.dumps({"request": 2})
                await websocket.send(json_response)
                print("Answered - Recalibration Done!")

            elif json_message["request"] == 12:
                # handle start game
                CALIBRATION_DONE.wait()
                json_response = json.dumps({"request": 2})
                await websocket.send(json_response)
                print("Answered - Calibration Done!")

            elif json_message["request"] == 13:
                # handle start of next round
                reset_image_count()
                ROUND_DONE.set()
                print("Started next Round!")
            elif json_message["request"] == 404:
                print("Error Wrong Request!")
            else:
                json_response = json.dumps({"request": 404})
                await websocket.send(json_response)
                print("Error Wrong Command!")
    except:
        print("Ups something went wrong! Client Disconnected")
    finally:
        CONNECTIONS.remove(websocket)

async def async_send_changes(json_message):
    global CONNECTIONS
    for sock in CONNECTIONS:
        await sock.send(json_message)

def send_changes(json_message):
    json_msg = json.dumps(json_message)
    asyncio.run(async_send_changes(json_msg))

