import time
import random
import os
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

print("TX BOT START")

while True:

    result = random.choice(["Tài", "Xỉu"])

    msg = f"""
🎲 AI TÀI XỈU

Dự đoán phiên tiếp:
{result}
"""

    bot.send_message(chat_id=CHAT_ID, text=msg)

    print("Sent:", result)

    time.sleep(60)
