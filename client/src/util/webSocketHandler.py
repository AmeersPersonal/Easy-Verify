import asyncio
import time
import websockets

connectionStatus = True

def setConnectionStatus(status):
    global connectionStatus
    connectionStatus = status
async def endWebsocket(server):

    setConnectionStatus(False)

async def handler(websocket):
    #TODO: Find way to elegantly close websocket, without giving an exception in the console, when the application is closed. Currently it just prints "Connection closed" in the console which is not ideal but it works for now.

    print("Client connected")
    try:
        message = await websocket.recv()
        print(f"Received message: {message}")
        
        await websocket.send(f"Message received: {message}")
        await websocket.send("Verification complete")

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        print("Connection closed")

async def openSocket():
    print("Starting WebSocket server on ws://localhost:8765")
    async with websockets.serve(handler, "localhost", 8765) as server:
        print("WebSocket server started")
        if (not connectionStatus):
            print("Connection status is False, closing server")
            await server.close()
        await server.wait_closed()  # run forever or until closed