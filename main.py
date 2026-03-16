import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

history=[]
wins=0
loses=0
last_prediction=None

# =========================
# TÀI / XỈU
# =========================

def tx(n):

    if n>=11:
        return "T"
    else:
        return "X"

# =========================
# THÊM KẾT QUẢ
# =========================

def add_result(nums):

    global wins,loses,last_prediction

    for n in nums:

        try:

            r=tx(int(n))

            history.append(r)

            if last_prediction:

                if r==last_prediction:
                    wins+=1
                else:
                    loses+=1

        except:
            pass

    if len(history)>2000:
        history.pop(0)

# =========================
# PHÂN TÍCH PATTERN
# =========================

def detect_patterns():

    patterns={}

    for size in range(2,8):

        if len(history)<size+1:
            continue

        seq=tuple(history[-size:])

        t=0
        x=0

        for i in range(len(history)-size):

            if tuple(history[i:i+size])==seq:

                nxt=history[i+size]

                if nxt=="T":
                    t+=1
                else:
                    x+=1

        if t+x>0:
            patterns[seq]=(t,x)

    return patterns

# =========================
# AI PHÂN TÍCH
# =========================

def ai_predict():

    patterns=detect_patterns()

    score_t=0
    score_x=0

    for p in patterns.values():

        score_t+=p[0]
        score_x+=p[1]

    # cầu bệt
    if len(history)>=3:

        if history[-1]==history[-2]==history[-3]:

            if history[-1]=="T":
                score_x+=4
            else:
                score_t+=4

    # zigzag
    if len(history)>=4:

        seq=history[-4:]

        if seq==["T","X","T","X"]:
            score_t+=3

        if seq==["X","T","X","T"]:
            score_x+=3

    # thống kê tổng
    t=history.count("T")
    x=history.count("X")

    if t>x:
        score_x+=2
    else:
        score_t+=2

    # random nhỏ
    score_t+=random.randint(0,2)
    score_x+=random.randint(0,2)

    total=score_t+score_x

    if total==0:
        return 50,50

    tai=int(score_t/total*100)
    xiu=100-tai

    return tai,xiu

# =========================
# GIAO DIỆN
# =========================

def ui(tai,xiu):

    global last_prediction

    result="TÀI" if tai>xiu else "XỈU"

    last_prediction="T" if result=="TÀI" else "X"

    return f"""
╔══════════════════════╗
        🤖 AI CASINO
╚══════════════════════╝

📊 AI PHÂN TÍCH

TÀI  : {tai}%
XỈU  : {xiu}%

━━━━━━━━━━━━━━

🎯 DỰ ĐOÁN

{result}

━━━━━━━━━━━━━━

🏆 WIN  : {wins}
❌ LOSE : {loses}

📚 DATA : {len(history)} round
"""

# =========================
# START
# =========================

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

"""
🤖 AI TX BOT

Nhập kết quả:

12

hoặc

14-15-16

/reset để reset dữ liệu
"""
)

# =========================
# RESET
# =========================

async def reset(update:Update,context:ContextTypes.DEFAULT_TYPE):

    global wins,loses

    history.clear()

    wins=0
    loses=0

    await update.message.reply_text("Đã reset dữ liệu")

# =========================
# NHẬP DỮ LIỆU
# =========================

async def text(update:Update,context:ContextTypes.DEFAULT_TYPE):

    msg=update.message.text

    nums=msg.replace(" ","").split("-")

    add_result(nums)

    tai,xiu=ai_predict()

    await update.message.reply_text(ui(tai,xiu))

# =========================
# RUN BOT
# =========================

app=ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("reset",reset))
app.add_handler(MessageHandler(filters.TEXT,text))

print("BOT AI RUNNING")

app.run_polling()
