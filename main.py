import json
import time
import websocket
import threading
from telegram import Bot

TOKEN = "BOT_TOKEN"
CHAT_ID = "CHAT_ID"

bot = Bot(TOKEN)

history = []

def analyze():
    if len(history) < 5:
        return "Đang phân tích..."

    last = history[-1]
    last2 = history[-2]

    if last == last2:
        return last
    else:
        return "Tài"

def send_signal():
    predict = analyze()

    msg = f"""
📊 AI TÀI XỈU

Lịch sử:
{history[-10:]}

🔮 Dự đoán phiên tiếp:
👉 {predict}
"""

    bot.send_message(chat_id=CHAT_ID,text=msg)

def on_message(ws,message):
    try:
        data = json.loads(message)

        if "dice" in data:

            dice = data["dice"]

            total = sum(dice)

            if total >= 11:
                result = "Tài"
            else:
                result = "Xỉu"

            history.append(result)

            if len(history) > 500:
                history.pop(0)

            send_signal()

    except:
        pass

def on_open(ws):
    print("Connected WebSocket")

socket = "wss://www.wss8888.com/mqtt"

ws = websocket.WebSocketApp(
    socket,
    on_message=on_message
)

ws.run_forever()
