import asyncio
import websockets
import ssl
import os

WS_URL = "wss://www.wss8888.com/mqtt"

async def connect():
    while True:
        try:
            print("Connecting to server...")

            async with websockets.connect(
                WS_URL,
                subprotocols=["mqttv3.1"]
            ) as ws:

                print("Connected!")

                while True:
                    data = await ws.recv()

                    print("DATA:", data)

        except Exception as e:
            print("Reconnect...", e)
            await asyncio.sleep(5)

asyncio.run(connect())
