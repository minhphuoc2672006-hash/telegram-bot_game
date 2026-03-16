import asyncio
import websockets
import ssl

WS_URL = "wss://www.wss8888.com/mqtt"

TOPICS = [
    "game/tx",
    "game/tx/result",
    "tx/result",
    "taixiu/result"
]

client_id = "railwaybot"


def build_connect():
    payload = bytearray()

    payload.extend([0x00,0x04])
    payload.extend(b"MQTT")

    payload.extend([0x04])
    payload.extend([0x02])

    payload.extend([0x00,0x3C])

    payload.extend([0x00,len(client_id)])
    payload.extend(client_id.encode())

    packet = bytearray()
    packet.append(0x10)
    packet.append(len(payload))
    packet.extend(payload)

    return packet


def build_sub(topic,pid):

    t = topic.encode()

    packet = bytearray()

    packet.append(0x82)
    packet.append(len(t)+5)

    packet.extend([0x00,pid])
    packet.extend([0x00,len(t)])
    packet.extend(t)

    packet.append(0x00)

    return packet


async def ping(ws):

    while True:

        await asyncio.sleep(20)

        try:

            await ws.send(b'\xc0\x00')

            print("PING")

        except:

            break


async def run():

    while True:

        try:

            print("Connecting...")

            async with websockets.connect(
                WS_URL,
                subprotocols=["mqttv3.1"],
                extra_headers={
                    "Origin":"https://www.luckywin882.com"
                }
            ) as ws:

                print("Connected")

                await ws.send(build_connect())

                print("CONNECT sent")

                resp = await ws.recv()

                print("CONNACK:",resp)

                pid = 1

                for t in TOPICS:

                    await ws.send(build_sub(t,pid))

                    print("SUB:",t)

                    pid += 1


                asyncio.create_task(ping(ws))

                while True:

                    data = await ws.recv()

                    print("DATA:",data)


        except Exception as e:

            print("ERROR:",e)

            await asyncio.sleep(5)


asyncio.run(run())
