import asyncio
import websockets
import base64
import requests
import os

# =========================
# TELEGRAM
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(msg):

    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram chưa cấu hình")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        requests.post(url,data={
            "chat_id":CHAT_ID,
            "text":msg
        })
    except:
        pass


# =========================
# SERVER
# =========================

WS_URL = "wss://www.wss8888.com/mqtt"

headers = {
    "Origin": "https://www.luckywin882.com",
    "User-Agent": "Mozilla/5.0"
}


# =========================
# AI HISTORY
# =========================

history = []

def analyze(total):

    history.append(total)

    if len(history) > 100:
        history.pop(0)

    tai = sum(1 for x in history if x >= 11)
    xiu = sum(1 for x in history if x <= 10)

    if tai > xiu:
        return "TÀI"
    else:
        return "XỈU"


# =========================
# DECODE DATA
# =========================

def decode_packet(data):

    try:

        text = data.decode(errors="ignore")

        if "game/push" not in text:
            return None

        start = text.find("game/push")

        payload = text[start+9:]

        decoded = base64.b64decode(payload)

        if len(decoded) > 10:

            d1 = decoded[-3] % 6 + 1
            d2 = decoded[-2] % 6 + 1
            d3 = decoded[-1] % 6 + 1

            return d1,d2,d3

    except:
        pass

    return None


# =========================
# LISTENER
# =========================

async def listen():

    while True:

        try:

            print("Connecting...")

            async with websockets.connect(
                WS_URL,
                additional_headers=headers,
                subprotocols=["mqtt"]
            ) as ws:

                print("Connected!")

                send_telegram("BOT ĐÃ KẾT NỐI SERVER")

                while True:

                    data = await ws.recv()

                    if isinstance(data,str):
                        data = data.encode()

                    result = decode_packet(data)

                    if result:

                        d1,d2,d3 = result

                        total = d1+d2+d3

                        prediction = analyze(total)

                        msg = f"""
🎲 KẾT QUẢ

{d1} - {d2} - {d3}

Tổng: {total}

AI dự đoán: {prediction}
"""

                        print(msg)

                        send_telegram(msg)

        except Exception as e:

            print("Reconnect...",e)

            await asyncio.sleep(5)


# =========================
# START
# =========================

print("BOT STARTED")

asyncio.run(listen())
