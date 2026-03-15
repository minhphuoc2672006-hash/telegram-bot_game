import websocket
import threading
import json
import base64
import gzip
import time
import random

WS_URL = "wss://www.wss8888.com/mqtt"

bot = None
CHAT_ID = None

history = []


def predict():

    if len(history) < 6:
        return "Chưa đủ dữ liệu"

    tai = history.count("T")
    xiu = history.count("X")

    if tai > xiu:
        return "➡️ AI dự đoán: XỈU"
    else:
        return "➡️ AI dự đoán: TÀI"


def send_result(d1, d2, d3):

    total = d1 + d2 + d3

    if total >= 11:
        kq = "TÀI"
        history.append("T")
    else:
        kq = "XỈU"
        history.append("X")

    ai = predict()

    text = f"""
🎲 KẾT QUẢ MỚI

{d1}-{d2}-{d3}

Tổng: {total}

➡️ {kq}

{ai}
"""

    if bot and CHAT_ID:
        bot.send_message(CHAT_ID, text)


def decode_message(msg):

    try:

        data = base64.b64decode(msg)

        data = gzip.decompress(data)

        return data

    except:

        return None


def on_message(ws, message):

    decoded = decode_message(message)

    if decoded:

        text = decoded.decode("utf-8", errors="ignore")

        if "dice" in text:

            # demo đọc xúc xắc
            d1 = random.randint(1,6)
            d2 = random.randint(1,6)
            d3 = random.randint(1,6)

            send_result(d1, d2, d3)


def on_open(ws):

    print("WebSocket Connected")


def run_ws():

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


def start(bot_instance, chat_id):

    global bot
    global CHAT_ID

    bot = bot_instance
    CHAT_ID = chat_id

    threading.Thread(target=run_ws).start()
