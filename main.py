import asyncio
import websockets
import os

WS_URL = "wss://www.wss8888.com/mqtt"

TOKEN = "PUT_YOUR_TOKEN_HERE"

CLIENT_ID = "tx_ai_bot"

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


def decode_game(data):

    try:

        nums = []

        for b in data:

            if 1 <= b <= 6:
                nums.append(b)

        if len(nums) >= 3:

            d1 = nums[-3]
            d2 = nums[-2]
            d3 = nums[-1]

            total = d1 + d2 + d3

            if total >= 11:
                result = "TÀI"
            else:
                result = "XỈU"

            print("🎲 Dice:",d1,d2,d3,"=",total,result)

    except:
        pass


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
                    "Origin":"https://www.luckywin882.com",
                    "User-Agent":"Mozilla/5.0",
                    "Referer":f"https://www.luckywin882.com/?token={TOKEN}&gameType=bigSmallMD5&roomID=1"
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


                asyncio.create_task(ping(ws))


                while True:

                    data = await ws.recv()

                    if isinstance(data,bytes):

                        packet_type = data[0] >> 4

                        if packet_type == 3:

                            print("GAME PACKET")

                            decode_game(data)

                        elif packet_type == 13:

                            print("PINGRESP")

                        else:

                            print("OTHER:",data)

        except Exception as e:

            print("ERROR:",e)

            await asyncio.sleep(5)


asyncio.run(run())
