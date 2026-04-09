import asyncio
import time
import websockets
import json
import base64
from util.encryptKeys import encryptor



async def handler(websocket):
    try:
        print("Client connected")
        print("Sending Key")
        e = encryptor()
        await websocket.send(json.dumps(e.getPublicKeyPEM().decode('utf-8')))
        encryptedB64 = await websocket.recv()
        encrypted = base64.b64decode(encryptedB64.strip())
        apiAndAuth = e.decrypt(encrypted).decode()
        print("got cyphertext")
        print(apiAndAuth)

        #INSERT THE START AND END OF VERIFICAITON HERE

        #PUT AN AWAIT HERE
        #AFTER VERIFICATION, SEND A CURL REQUEST TO THE API URL SENT BY THE apiAndAuth

        #TODO:
        await websocket.send("Verification complete")
        print("Transaction complete")
    except ValueError:
        print("Key Error")
    except Exception as err:
        print("Unexpected error")
        print(err)
    finally:
        await websocket.close()



async def openSocket():
    print("Starting WebSocket server on ws://localhost:8765")
    async with websockets.serve(handler, "localhost", 8765) as server:
        print("WebSocket server started")
        await server.wait_closed()  # run forever or until closed
    return True
