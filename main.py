import asyncio
import websockets

WS_URL = "wss://www.wss8888.com/mqtt"
CLIENT_ID = "railway_tx_bot"

TOPICS = [
    "game/#",
    "taixiu/#",
    "tx/#"
]


def build_connect():

    payload = bytearray()

    payload.extend([0x00,0x04])
    payload.extend(b"MQTT")

    payload.append(0x04)
    payload.append(0x02)

    payload.extend([0x00,60])

    payload.extend([0x00,len(CLIENT_ID)])
    payload.extend(CLIENT_ID.encode())

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


def build_publish(topic,message):

    t = topic.encode()
    m = message.encode()

    packet = bytearray()

    packet.append(0x30)

    remaining = len(t) + len(m) + 2
    packet.append(remaining)

    packet.extend([0x00,len(t)])
    packet.extend(t)

    packet.extend(m)

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

                for topic in TOPICS:

                    await ws.send(build_sub(topic,pid))

                    print("SUB:",topic)

                    pid += 1


                await ws.send(build_publish("game/join","taixiu"))
                print("JOIN TAIXIU ROOM")


                asyncio.create_task(ping(ws))


                while True:

                    data = await ws.recv()

                    if isinstance(data, bytes):

                        packet_type = data[0] >> 4

                        if packet_type == 3:

                            print("GAME DATA:", data)

                        elif packet_type == 13:

                            print("PINGRESP")

                        else:

                            print("OTHER:",data)

                    else:

                        print("TEXT:",data)

        except Exception as e:

            print("ERROR:",e)

            await asyncio.sleep(5)


asyncio.run(run())
