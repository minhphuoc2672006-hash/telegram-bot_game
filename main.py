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

                data = await ws.recv()
                print("CONNACK:",data)

                # SUBSCRIBE topic
                subscribe_packet = bytes([
                    0x82,0x0F,
                    0x00,0x01,
                    0x00,0x0A,
                    0x74,0x61,0x69,0x78,0x69,0x75,0x2F,0x64,0x61,0x74,0x61,
                    0x00
                ])

                await ws.send(subscribe_packet)

                print("SUBSCRIBE sent")

                while True:

                    data = await ws.recv()

                    print("DATA:",data)

        except Exception as e:

            print("Reconnect...",e)

            await asyncio.sleep(5)


asyncio.run(connect())
