# Websocket Library https://websockets.readthedocs.io/en/stable/
import urllib.request
import urllib
import json
import asyncio
import websockets

urlPath = "http://localhost:3000/api/post"
data = {
    "name": "Test",
    "key": "123123123"
}

dataparsed = json.dumps(data)
dataencoded = dataparsed.encode('utf-8')

req = urllib.request.Request(
    "http://localhost:3000/api/post",
    data=dataencoded,
    headers={"Content-Type": "application/json"},
    method="POST"
)

def sendRequest():
    print(dataparsed)

    with urllib.request.urlopen(req) as request:
        print(request.read(300))
        
sendRequest()