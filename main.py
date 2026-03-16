import asyncio
import websockets

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

                # MQTT CONNECT
                connect_packet = bytes([
                    0x10,0x12,
                    0x00,0x04,0x4D,0x51,0x54,0x54,
                    0x04,
                    0x02,
                    0x00,0x3C,
                    0x00,0x04,0x62,0x6F,0x74,0x31
                ])

                await ws.send(connect_packet)

                print("MQTT CONNECT sent")

                while True:
                    data = await ws.recv()
                    print("DATA:", data)

        except Exception as e:
            print("Reconnect...", e)
            await asyncio.sleep(5)

asyncio.run(connect())
