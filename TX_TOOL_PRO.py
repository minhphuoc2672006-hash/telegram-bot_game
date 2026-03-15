import websocket
import base64
import gzip
import json
import time

WS_URL = "wss://www.wss8888.com/mqtt"

history = []

def decode_payload(data):
    try:
        raw = base64.b64decode(data)
        raw = gzip.decompress(raw)
        return raw.decode()
    except:
        return None

def parse_result(text):
    try:
        data = json.loads(text)

        d1 = data["dice1"]
        d2 = data["dice2"]
        d3 = data["dice3"]

        total = d1+d2+d3

        if total >= 11:
            result = "TAI"
        else:
            result = "XIU"

        history.append(result)

        print("Dice:",d1,d2,d3)
        print("Total:",total,result)
        print("History:",history[-20:])

    except:
        pass


def on_message(ws,message):

    if "game/pushtz" in str(message):

        payload = str(message).split("game/pushtz")[-1]

        decoded = decode_payload(payload)

        if decoded:
            print("RAW:",decoded)
            parse_result(decoded)


def on_open(ws):
    print("Connected")


while True:

    try:

        ws = websocket.WebSocketApp(
            WS_URL,
            on_open=on_open,
            on_message=on_message
        )

        ws.run_forever()

    except:
        print("Reconnect...")
        time.sleep(5)
