import asyncio
import websockets
import json
import requests
import os

# ==========================
# TELEGRAM
# ==========================

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, data=data)

# ==========================
# GAME SOCKET
# ==========================

WS_URL = "wss://ws.luckywin882.com/websocket"

async def connect():
    while True:
        try:
            async with websockets.connect(WS_URL) as ws:
                print("Connected to game server")

                while True:
                    data = await ws.recv()
                    print("DATA:", data)

                    try:
                        msg = json.loads(data)

                        if "result" in msg:
                            result = msg["result"]
                            send_telegram(f"Kết quả: {result}")

                    except:
                        pass

        except Exception as e:
            print("Reconnect...", e)
            await asyncio.sleep(5)

# ==========================
# START
# ==========================

asyncio.run(connect())
