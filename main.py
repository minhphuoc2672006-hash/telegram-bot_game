import telebot
import os
import TX_TOOL_PRO

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(
        message.chat.id,
        """
🤖 AI CASINO TOOL

BOT AUTO ĐANG CHẠY

Đang kết nối WebSocket...
"""
    )

    TX_TOOL_PRO.start(bot, message.chat.id)


print("BOT START")

bot.infinity_polling()
