import asyncio
import websockets

WS_URL = "wss://www.wss8888.com/mqtt"

async def mqtt_connect():

    async with websockets.connect(
        WS_URL,
        subprotocols=["mqttv3.1"],
        extra_headers={
            "Origin":"https://www.luckywin882.com"
        }
    ) as ws:

        print("Connected")

        # MQTT CONNECT
        packet = bytes([
        0x10,0x16,
        0x00,0x04,0x4d,0x51,0x54,0x54,
        0x04,
        0x02,
        0x00,0x3c,
        0x00,0x0c
        ]) + b"railway-bot"

        await ws.send(packet)

        print("CONNECT sent")

        resp = await ws.recv()
        print("CONNACK:",resp)


        topics = [
        "game/tx",
        "game/tx/result",
        "tx/result",
        "taixiu/result"
        ]


        pid = 1

        for topic in topics:

            topic_b = topic.encode()

            subscribe = bytes([
            0x82,
            len(topic_b)+5,
            0x00,pid,
            0x00,len(topic_b)
            ]) + topic_b + bytes([0x00])

            await ws.send(subscribe)

            print("SUB:",topic)

            pid+=1


        while True:

            data = await ws.recv()

            print("DATA:",data)


asyncio.run(mqtt_connect())
