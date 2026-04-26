import asyncio
from ssl import ALERT_DESCRIPTION_USER_CANCELLED
import websockets
import json
import base64
import threading
from util.client import Client
from util.encryptKeys import encryptor
from util.webRequest import sendPost

wsLoop = None
verifyEvent = threading.Event()
isConnected = False


async def handler(websocket):
    try:
        global isConnected
        isConnected = True

        print("Client connected")
        print("Sending Key")
        e = encryptor()
        sendData = {'responseType': 'public_key', 'response': e.getPublicKeyPEM().decode("utf-8")}
        await websocket.send(json.dumps(sendData))

        jsonRecieved = await websocket.recv()
        encryptedB64 = json.loads(jsonRecieved)['message']
        print(encryptedB64)
        encrypted = base64.b64decode(encryptedB64.strip())
        apiAndAuth = e.decrypt(encrypted).decode()
        print("got cyphertext and decrypted it")
        print(apiAndAuth)

        userClient = Client(json.loads(apiAndAuth))
        userClient.printAttrib()  # temporary

        verifyEvent.wait()
        print("sending verification to api")
        verifcationReq = {'email': userClient.email}
        sendPost(verifcationReq, userClient.callback_url)


        verifyDone = {'responseType': 'verifyStatus', 'response': 'OK'}
        await websocket.send(json.dumps(verifyDone))
        print("Transaction complete")
    except ValueError:
        print("Key Error")
    except Exception as err:
        print("Unexpected error")
        print(err)
    finally:
        print("closing socket")
        await websocket.close()
        stopSocket()


async def openSocket():
    async with websockets.serve(handler, "localhost", 8765) as server:
        print("Starting WebSocket server on ws://localhost:8765")
        print("Server is now listening")
        global wsLoop
        wsLoop = asyncio.get_running_loop()
        await server.wait_closed()  # run forever or until closed
    return True


def stopSocket():
    if (
        wsLoop and wsLoop.is_running()
    ):  # get the loop then end it gracefully on app close
        print("closing")
        wsLoop.call_soon_threadsafe(wsLoop.stop)


def finishVerify():
    if wsLoop and wsLoop.is_running() and isConnected:
        verifyEvent.set()
    if not isConnected:
        print("Nothing connected")
