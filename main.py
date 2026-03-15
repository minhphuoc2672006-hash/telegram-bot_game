import telebot
import hashlib
import random
import os

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("BOT_TOKEN not found")
    exit()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle(message):

    text = message.text

    h = hashlib.md5(text.encode()).hexdigest()
    num = int(h[:2],16) % 16 + 3

    if num >= 11:
        result = "TÀI"
    else:
        result = "XỈU"

    percent = random.randint(60,90)

    bot.reply_to(message,f"""
🎲 AI TÀI XỈU

Kết quả: {result}
Tỷ lệ: {percent}%
""")

print("BOT STARTED")
bot.infinity_polling()
