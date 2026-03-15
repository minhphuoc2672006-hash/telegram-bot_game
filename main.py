import telebot
import hashlib
import random
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle(message):
    text = str(message.text)

    h = hashlib.md5(text.encode()).hexdigest()
    num = int(h[:2],16) % 16 + 3

    if 3 <= num <= 10:
        result = "TÀI"
    else:
        result = "XỈU"

    percent = random.randint(60,90)

    bot.reply_to(message,
f"""🎲 AI TÀI XỈU

Kết quả: {result}
Tỷ lệ: {percent}%""")

print("BOT ĐANG CHẠY...")

bot.infinity_polling()
