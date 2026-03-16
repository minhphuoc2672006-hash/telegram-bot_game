import asyncio
import websockets
import json
import requests
import os

# =========================
# TELEGRAM CONFIG (AN TOÀN)
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# WEBSOCKET SERVER
# =========================

WS_URL = "wss://www.wss8888.com/mqtt"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://www.w88.com"
}

# =========================
# SEND TELEGRAM
# =========================

def send_telegram(msg):

    if not BOT_TOKEN or not CHAT_ID:
        print("Missing TELEGRAM CONFIG")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print("Telegram error:", e)

# =========================
# PHÂN TÍCH TÀI XỈU
# =========================

history = []

def analyze(result):

    history.append(result)

    if len(history) > 50:
        history.pop(0)

    tai = sum(1 for x in history if x >= 11)
    xiu = sum(1 for x in history if x <= 10)

    if tai > xiu:
        return "TÀI"
    else:
        return "XỈU"

# =========================
# WEBSOCKET LISTENER
# =========================

async def listen():

    while True:

        try:

            print("Connecting websocket...")

            async with websockets.connect(
                WS_URL,
                additional_headers=headers
            ) as ws:

                print("Connected!")

                send_telegram("🤖 BOT ĐÃ KẾT NỐI SERVER")

                while True:

                    data = await ws.recv()

                    print("DATA:", data)

                    try:

                        msg = json.loads(data)

                        if "dice" in msg:

                            d1, d2, d3 = msg["dice"]

                            total = d1 + d2 + d3

                            prediction = analyze(total)

                            text = f"""
🎲 KẾT QUẢ

{d1} - {d2} - {d3}

Tổng: {total}

AI dự đoán: {prediction}
"""

                            send_telegram(text)

                    except Exception as e:
                        print("Parse error:", e)

        except Exception as e:

            print("Reconnect...", e)

            await asyncio.sleep(5)

# =========================
# MAIN
# =========================

print("🚀 BOT STARTED")

asyncio.run(listen())
