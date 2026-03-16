import os
import json
import websocket
import threading
import time
from telegram import Bot

# =========================
# TELEGRAM CONFIG
# =========================

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(TOKEN)

# =========================
# DATA STORAGE
# =========================

history = []
sessions = []

MAX_HISTORY = 500

# =========================
# TÀI XỈU LOGIC
# =========================

def tai_xiu(total):
    if total >= 11:
        return "Tài"
    else:
        return "Xỉu"

# =========================
# BIG ROAD ANALYSIS
# =========================

def big_road():

    road = []
    column = []

    for r in history:

        if not column:
            column.append(r)

        elif column[-1] == r:
            column.append(r)

        else:
            road.append(column)
            column = [r]

    if column:
        road.append(column)

    return road

# =========================
# PREDICTION
# =========================

def predict():

    if len(history) < 6:
        return "Đang phân tích..."

    last = history[-1]
    last2 = history[-2]
    last3 = history[-3]

    # cầu bệt
    if last == last2 == last3:
        return last

    # cầu đảo
    if last != last2:
        return last2

    # fallback
    return last

# =========================
# TELEGRAM MESSAGE
# =========================

def send_signal():

    try:

        road = big_road()
        du_doan = predict()

        last10 = history[-10:]

        msg = f"""
📊 AI TÀI XỈU

10 phiên gần nhất
{last10}

📈 Big Road columns
{len(road)}

🔮 Dự đoán phiên tiếp
👉 {du_doan}
"""

        bot.send_message(chat_id=CHAT_ID, text=msg)

    except Exception as e:
        print("Telegram error:", e)

# =========================
# PROCESS GAME DATA
# =========================

def process_data(data):

    try:

        if "dice" in data:

            dice = data["dice"]

            total = sum(dice)

            result = tai_xiu(total)

            history.append(result)

            if len(history) > MAX_HISTORY:
                history.pop(0)

            print("Dice:", dice, "=", result)

            send_signal()

    except:
        pass

# =========================
# WEBSOCKET EVENTS
# =========================

def on_message(ws, message):

    try:

        print("RAW:", message)

        data = json.loads(message)

        process_data(data)

    except:
        pass


def on_error(ws, error):
    print("ERROR:", error)


def on_close(ws, close_status_code, close_msg):
    print("### CONNECTION CLOSED ###")

    time.sleep(5)

    start_ws()


def on_open(ws):
    print("### CONNECTED GAME SERVER ###")

# =========================
# CONNECT GAME SERVER
# =========================

def start_ws():

    socket = "wss://www.wss8888.com/mqtt"

    ws = websocket.WebSocketApp(
        socket,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever()

# =========================
# START BOT
# =========================

if __name__ == "__main__":

    print("🚀 AI TÀI XỈU BOT START")

    start_ws()
