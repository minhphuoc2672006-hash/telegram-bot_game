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

                connack = await ws.recv()
                print("CONNACK:",connack)

                # SUBSCRIBE topic
                topic = "taixiu/data"
                topic_bytes = topic.encode()

                subscribe_packet = bytes([
                    0x82,
                    len(topic_bytes)+5,
                    0x00,0x01,
                    0x00,len(topic_bytes)
                ]) + topic_bytes + bytes([0x00])

                await ws.send(subscribe_packet)

                print("SUBSCRIBE sent")

                # giữ kết nối và đọc dữ liệu
                while True:

                    data = await ws.recv()

                    print("DATA:",data)

        except Exception as e:

            print("Reconnect...",e)

            await asyncio.sleep(5)


asyncio.run(connect())
