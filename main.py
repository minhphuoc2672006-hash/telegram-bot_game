import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN=os.getenv("BOT_TOKEN")

history=[]
wins=0
loses=0
last_prediction=None

# =========================
# TÀI XỈU
# =========================

def tx(n):
    return "T" if n>=11 else "X"

# =========================
# THÊM DỮ LIỆU
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

    if len(history)>5000:
        history.pop(0)

# =========================
# CẦU BỆT
# =========================

def cau_bet():

    if len(history)<3:
        return 0,0

    if history[-1]==history[-2]==history[-3]:

        if history[-1]=="T":
            return 0,5
        else:
            return 5,0

    return 0,0

# =========================
# CẦU ZIGZAG
# =========================

def cau_zigzag():

    if len(history)<4:
        return 0,0

    seq=history[-4:]

    if seq==["T","X","T","X"]:
        return 4,0

    if seq==["X","T","X","T"]:
        return 0,4

    return 0,0

# =========================
# CẦU PATTERN AI
# =========================

def pattern_ai():

    score_t=0
    score_x=0

    for size in range(2,7):

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

        score_t+=t
        score_x+=x

    return score_t,score_x

# =========================
# THỐNG KÊ LỊCH SỬ
# =========================

def statistics():

    t=history.count("T")
    x=history.count("X")

    if t>x:
        return 0,3
    else:
        return 3,0

# =========================
# AI DỰ ĐOÁN
# =========================

def ai_predict():

    score_t=0
    score_x=0

    a,b=pattern_ai()
    score_t+=a
    score_x+=b

    a,b=cau_bet()
    score_t+=a
    score_x+=b

    a,b=cau_zigzag()
    score_t+=a
    score_x+=b

    a,b=statistics()
    score_t+=a
    score_x+=b

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
        🤖 AI CASINO PRO
╚══════════════════════╝

📊 PHÂN TÍCH AI

TÀI  : {tai}%
XỈU  : {xiu}%

━━━━━━━━━━━━━━

🎯 DỰ ĐOÁN

{result}

━━━━━━━━━━━━━━

🏆 WIN  : {wins}
❌ LOSE : {loses}

📚 DATA : {len(history)} ROUND
"""

# =========================
# START
# =========================

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("""

🤖 AI TX BOT PRO

Nhập kết quả ví dụ:

12

hoặc

14-15-16

/reset reset dữ liệu
/stats xem thống kê
""")

# =========================
# RESET
# =========================

async def reset(update:Update,context:ContextTypes.DEFAULT_TYPE):

    global history,wins,loses,last_prediction

    history.clear()
    wins=0
    loses=0
    last_prediction=None

    await update.message.reply_text("Đã reset dữ liệu AI")

# =========================
# STATS
# =========================

async def stats(update:Update,context:ContextTypes.DEFAULT_TYPE):

    t=history.count("T")
    x=history.count("X")

    await update.message.reply_text(f"""

📊 THỐNG KÊ

TÀI : {t}
XỈU : {x}

WIN : {wins}
LOSE : {loses}

DATA : {len(history)}
""")

# =========================
# NHẬP DATA
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
app.add_handler(CommandHandler("stats",stats))
app.add_handler(MessageHandler(filters.TEXT,text))

print("AI CASINO BOT RUNNING")

app.run_polling()
