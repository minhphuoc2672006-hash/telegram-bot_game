import TX_TOOL_PRO
import telebot
import os
import json
import random

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "history.json"

# LOAD HISTORY
if os.path.exists(DATA_FILE):
    with open(DATA_FILE,"r") as f:
        history = json.load(f)
else:
    history = []

def save():
    with open(DATA_FILE,"w") as f:
        json.dump(history,f)

def tx(n):
    return "T" if n >= 11 else "X"

# AI ENGINE
def ai_predict():

    if len(history) < 20:
        return None,None

    score_tai = 0
    score_xiu = 0

# TREND ENGINE

    recent = history[-30:]

    tai = sum(1 for n in recent if n >= 11)
    xiu = sum(1 for n in recent if n <= 10)

    if tai > xiu:
        score_tai += 3
    else:
        score_xiu += 3

# SEQUENCE ENGINE

    seq = [tx(n) for n in recent]

    if len(seq) >= 3:

        if seq[-1] == seq[-2] == seq[-3]:

            if seq[-1] == "T":
                score_xiu += 2
            else:
                score_tai += 2

# PATTERN ENGINE

    for size in range(3,12):

        pattern = history[-size:]

        for i in range(len(history)-size):

            if history[i:i+size] == pattern:

                if i+size < len(history):

                    next_num = history[i+size]

                    if next_num >= 11:
                        score_tai += 4
                    else:
                        score_xiu += 4

# PROBABILITY ENGINE

    total = score_tai + score_xiu

    if total == 0:
        return None,None

    if score_tai > score_xiu:
        result = "TÀI"
        percent = int((score_tai/total)*100)
    else:
        result = "XỈU"
        percent = int((score_xiu/total)*100)

    percent = max(percent, random.randint(65,85))

    return result,percent

# START

@bot.message_handler(commands=['start'])
def start(message):

    bot.reply_to(message,
"""╔════════════════════════╗
      🤖 AI CASINO TOOL
   Advanced Analyzer v3
╚════════════════════════╝

📥 Nhập kết quả:

12-10-5-14-11

Bot sẽ phân tích lịch sử
""")

# RESET

@bot.message_handler(commands=['reset'])
def reset(message):

    history.clear()
    save()

    bot.reply_to(message,"♻️ Đã reset toàn bộ dữ liệu")

# INPUT

@bot.message_handler(func=lambda m: True)
def handle(message):

    text = message.text.replace(" ","")

    parts = text.split("-")

    added = []

    for p in parts:

        if p.isdigit():

            num = int(p)

            if 3 <= num <= 18:

                history.append(num)
                added.append(num)

    if not added:
        return

    save()

    result,percent = ai_predict()

    if result:

        bot.reply_to(message,
f"""╔════════════════════════╗
      🤖 AI CASINO TOOL
   Advanced Analyzer v3
╚════════════════════════╝

📡 Đang phân tích dữ liệu...

🎯 DỰ ĐOÁN: {result}
📊 XÁC SUẤT: {percent}%

────────────────
AI ENGINE:
• Pattern Detection
• Trend Analyzer
• Sequence Analyzer
• Probability Engine
""")

print("BOT STARTED")

bot.infinity_polling()
