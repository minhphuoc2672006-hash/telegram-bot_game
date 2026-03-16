import os
import random
from collections import defaultdict
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN=os.getenv("BOT_TOKEN")

history=[]
wins=0
loses=0
last_prediction=None

MAX_HISTORY=20000

# =========================
# TÀI XỈU
# =========================

def tx(n):
    return "T" if n>=11 else "X"

# =========================
# ADD RESULT
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

    if len(history)>MAX_HISTORY:
        history.pop(0)

# =========================
# CẦU BỆT
# =========================

def cau_bet():

    if len(history)<4:
        return 0,0

    last=history[-1]
    count=1

    for i in range(len(history)-2,-1,-1):

        if history[i]==last:
            count+=1
        else:
            break

    if count>=3:

        if last=="T":
            return 0,6
        else:
            return 6,0

    return 0,0

# =========================
# ZIGZAG
# =========================

def cau_zigzag():

    if len(history)<5:
        return 0,0

    seq=history[-5:]

    if seq==["T","X","T","X","T"]:
        return 0,5

    if seq==["X","T","X","T","X"]:
        return 5,0

    return 0,0

# =========================
# ĐẢO CẦU
# =========================

def cau_dao():

    if len(history)<2:
        return 0,0

    if history[-1]=="T":
        return 0,2
    else:
        return 2,0

# =========================
# PATTERN AI
# =========================

def pattern_ai():

    score_t=0
    score_x=0

    for size in range(2,12):

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
# MARKOV
# =========================

def markov():

    t=0
    x=0

    for i in range(len(history)-1):

        if history[i]=="T":

            if history[i+1]=="T":
                t+=1
            else:
                x+=1

        if history[i]=="X":

            if history[i+1]=="X":
                x+=1
            else:
                t+=1

    return t,x

# =========================
# MONTE CARLO
# =========================

def monte_carlo():

    t=0
    x=0

    if len(history)<10:
        return 0,0

    for _ in range(500):

        r=random.choice(history)

        if r=="T":
            t+=1
        else:
            x+=1

    return t,x

# =========================
# STATISTICS
# =========================

def statistics():

    t=history.count("T")
    x=history.count("X")

    if t>x:
        return 0,3
    else:
        return 3,0

# =========================
# AI ENGINE
# =========================

def ai_predict():

    score_t=0
    score_x=0

    engines=[
        pattern_ai,
        markov,
        monte_carlo,
        cau_bet,
        cau_zigzag,
        cau_dao,
        statistics
    ]

    for e in engines:

        a,b=e()

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
# UI
# =========================

def ui(tai,xiu):

    global last_prediction

    result="TÀI" if tai>xiu else "XỈU"

    last_prediction="T" if result=="TÀI" else "X"

    rounds=wins+loses

    wr=0
    if rounds>0:
        wr=int(wins/rounds*100)

    return f"""
╔══════════════════════╗
      🤖 AI CASINO PRO
╚══════════════════════╝

📊 AI ANALYSIS

TÀI : {tai}%
XỈU : {xiu}%

━━━━━━━━━━━━━━

🎯 SIGNAL

🔥 {result}

━━━━━━━━━━━━━━

🏆 WIN  : {wins}
❌ LOSE : {loses}
📈 WR   : {wr}%

📚 DATA : {len(history)}
"""

# =========================
# TELEGRAM COMMAND
# =========================

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("""
🤖 AI TX BOT

Nhập kết quả:

12
hoặc
12-14-15

/reset reset bot
/stats xem thống kê
""")

async def reset(update:Update,context:ContextTypes.DEFAULT_TYPE):

    global history,wins,loses,last_prediction

    history.clear()
    wins=0
    loses=0
    last_prediction=None

    await update.message.reply_text("RESET DATA DONE")

async def stats(update:Update,context:ContextTypes.DEFAULT_TYPE):

    t=history.count("T")
    x=history.count("X")

    await update.message.reply_text(f"""

📊 STATS

TÀI : {t}
XỈU : {x}

WIN : {wins}
LOSE: {loses}

DATA : {len(history)}
""")

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
