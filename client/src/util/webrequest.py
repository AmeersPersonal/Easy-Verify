# Websocket Library https://websockets.readthedocs.io/en/stable/
import urllib.request
import urllib
import json
import asyncio
import websockets



def sendPost(data, urlPath):
    dataparsed = json.dumps(data)
    dataencoded = dataparsed.encode("utf-8")

    req = urllib.request.Request(
        urlPath,
        data=dataencoded,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    print(dataparsed)

    with urllib.request.urlopen(req) as request:
        print(request.read(300))
