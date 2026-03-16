import asyncio
import json
import os
import ssl
import websockets
import requests
from collections import deque

# =========================
# TELEGRAM CONFIG
# =========================

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)

# =========================
# GAME LOGIC
# =========================

history = deque(maxlen=500)

def tai_xiu(total):
    if total >= 11:
        return "TÀI"
    return "XỈU"

# =========================
# PHÂN TÍCH CẦU
# =========================

def analyze():
    if len(history) < 10:
        return "ĐANG THU THẬP DATA..."

    last = list(history)

    tai = last.count("TÀI")
    xiu = last.count("XỈU")

    streak = 1
    for i in range(len(last)-1,0,-1):
        if last[i] == last[i-1]:
            streak +=1
        else:
            break

    if streak >= 3:
        predict = "XỈU" if last[-1] == "TÀI" else "TÀI"
    else:
        predict = "TÀI" if tai > xiu else "XỈU"

    return predict

# =========================
# MQTT CONNECT
# =========================

async def connect():

    url = "wss://www.wss8888.com/mqtt"

    headers = {
        "Origin": "https://www.luckywin882.com",
        "User-Agent": "Mozilla/5.0",
    }

    async with websockets.connect(url, extra_headers=headers, ssl=ssl.SSLContext()) as ws:

        print("Connected MQTT")

        while True:

            msg = await ws.recv()

            try:

                data = json.loads(msg)

                if "dice" in data:

                    d1 = data["dice"][0]
                    d2 = data["dice"][1]
                    d3 = data["dice"][2]

                    total = d1+d2+d3

                    result = tai_xiu(total)

                    history.append(result)

                    predict = analyze()

                    text = f"""
🎲 KẾT QUẢ

Xúc xắc: {d1}-{d2}-{d3}
Tổng: {total}

➡ {result}

📊 Phiên tiếp theo dự đoán:

🔥 {predict}
"""

                    print(text)

                    send_telegram(text)

            except:
                pass


# =========================
# RUN BOT
# =========================

async def main():

    while True:
        try:
            await connect()
        except Exception as e:
            print("Reconnect...",e)
            await asyncio.sleep(5)

asyncio.run(main())
