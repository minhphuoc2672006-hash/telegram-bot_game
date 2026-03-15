import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

history = []

# ===== PHÂN TÍCH TOÀN BỘ LỊCH SỬ =====

def predict():

    if len(history) < 6:
        return "Chưa đủ dữ liệu để phân tích"

    pattern_len = 4
    pattern = history[-pattern_len:]

    matches = []

    for i in range(len(history) - pattern_len):

        if history[i:i+pattern_len] == pattern:

            if i + pattern_len < len(history):
                matches.append(history[i+pattern_len])

    if matches:

        tai = sum(1 for n in matches if n >= 11)
        xiu = sum(1 for n in matches if n <= 10)

        if tai > xiu:
            result = "TÀI"
        else:
            result = "XỈU"

        return f"🔎 AI tìm thấy {len(matches)} mẫu giống → dự đoán {result}"

    return "🔎 Không tìm thấy mẫu lặp trong lịch sử"

# ===== START =====

@bot.message_handler(commands=['start'])
def start(message):

    bot.reply_to(
        message,
        "🤖 TOOL AI TÀI XỈU\n\n"
        "Nhập số từ 3 đến 18\n"
        "/reset để xóa lịch sử\n"
        "/history để xem lịch sử"
    )

# ===== RESET =====

@bot.message_handler(commands=['reset'])
def reset(message):

    history.clear()

    bot.reply_to(message, "🔄 Đã reset toàn bộ lịch sử")

# ===== HISTORY =====

@bot.message_handler(commands=['history'])
def show_history(message):

    if not history:
        bot.reply_to(message, "Chưa có dữ liệu")
    else:
        bot.reply_to(message, f"Lịch sử:\n{history}")

# ===== NHẬP SỐ =====

@bot.message_handler(func=lambda m: m.text.isdigit())
def handle(message):

    num = int(message.text)

    if num < 3 or num > 18:
        bot.reply_to(message, "⚠️ Chỉ nhập số từ 3 đến 18")
        return

    history.append(num)

    if num >= 11:
        result = "TÀI"
    else:
        result = "XỈU"

    prediction = predict()

    bot.reply_to(
        message,
        f"""
🎲 TOOL AI TÀI XỈU

Kết quả: {result}

Tổng lịch sử: {len(history)}

{prediction}
"""
    )

# ===== RUN BOT =====

print("BOT STARTED")

bot.infinity_polling()
