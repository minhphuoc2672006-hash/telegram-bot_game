import os
from collections import defaultdict
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN=os.getenv("BOT_TOKEN")

history=[]
wins=0
loses=0
last_prediction=None

MAX_HISTORY=50000

# =====================
# TÀI XỈU
# =====================

def tx(n):
    return "T" if n>=11 else "X"

# =====================
# ADD DATA
# =====================

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

# =====================
# MARKOV LEVEL 1
# =====================

def markov1():

    t_to_t=0
    t_to_x=0
    x_to_t=0
    x_to_x=0

    for i in range(len(history)-1):

        a=history[i]
        b=history[i+1]

        if a=="T" and b=="T":
            t_to_t+=1

        if a=="T" and b=="X":
            t_to_x+=1

        if a=="X" and b=="T":
            x_to_t+=1

        if a=="X" and b=="X":
            x_to_x+=1

    score_t=0
    score_x=0

    if history[-1]=="T":
        score_t+=t_to_t
        score_x+=t_to_x
    else:
        score_t+=x_to_t
        score_x+=x_to_x

    return score_t,score_x

# =====================
# MARKOV LEVEL 2
# =====================

def markov2():

    if len(history)<3:
        return 0,0

    pattern=tuple(history[-2:])

    t=0
    x=0

    for i in range(len(history)-2):

        if tuple(history[i:i+2])==pattern:

            nxt=history[i+2]

            if nxt=="T":
                t+=1
            else:
                x+=1

    return t*2,x*2

# =====================
# PATTERN SCANNER
# =====================

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

        score_t+=t*size
        score_x+=x*size

    return score_t,score_x

# =====================
# STREAK
# =====================

def streak():

    if len(history)<3:
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
            return 0,count*2
        else:
            return count*2,0

    return 0,0

# =====================
# ZIGZAG
# =====================

def zigzag():

    if len(history)<5:
        return 0,0

    seq=history[-5:]

    if seq==["T","X","T","X","T"]:
        return 0,5

    if seq==["X","T","X","T","X"]:
        return 5,0

    return 0,0

# =====================
# BAYESIAN
# =====================

def bayes():

    t=history.count("T")
    x=history.count("X")

    total=t+x

    if total==0:
        return 0,0

    pt=t/total
    px=x/total

    return int(pt*10),int(px*10)

# =====================
# AI PREDICT
# =====================

def ai_predict():

    if len(history)<20:
        return 50,50,"NO DATA"

    score_t=0
    score_x=0

    engines=[

        markov1,
        markov2,
        pattern_ai,
        streak,
        zigzag,
        bayes

    ]

    for e in engines:

        a,b=e()

        score_t+=a
        score_x+=b

    total=score_t+score_x

    if total==0:
        return 50,50,"NO BET"

    tai=int(score_t/total*100)
    xiu=100-tai

    confidence=abs(tai-xiu)

    if confidence<10:
        signal="NO BET"

    elif tai>xiu:
        signal="TÀI"

    else:
        signal="XỈU"

    return tai,xiu,signal

# =====================
# UI
# =====================

def ui(tai,xiu,signal):

    global last_prediction

    if signal=="TÀI":
        last_prediction="T"

    elif signal=="XỈU":
        last_prediction="X"

    rounds=wins+loses

    wr=0
    if rounds>0:
        wr=int(wins/rounds*100)

    confidence=abs(tai-xiu)

    return f"""
╔══════════════════════╗
        🎰 AI TX PRO
╚══════════════════════╝

📊 ANALYSIS

TÀI : {tai}%
XỈU : {xiu}%

CONFIDENCE : {confidence}%

━━━━━━━━━━━━━━

🎯 SIGNAL

{signal}

━━━━━━━━━━━━━━

🏆 WIN : {wins}
❌ LOSE: {loses}
📈 WR  : {wr}%

📚 DATA : {len(history)}
"""

# =====================
# TELEGRAM
# =====================

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("""

🤖 AI TX BOT PRO

Nhập kết quả:

12

hoặc

12-14-16

/reset reset bot
/stats thống kê

""")

async def reset(update:Update,context:ContextTypes.DEFAULT_TYPE):

    global history,wins,loses,last_prediction

    history.clear()
    wins=0
    loses=0
    last_prediction=None

    await update.message.reply_text("RESET DONE")

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

    tai,xiu,signal=ai_predict()

    await update.message.reply_text(ui(tai,xiu,signal))

# =====================
# RUN
# =====================

app=ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("reset",reset))
app.add_handler(CommandHandler("stats",stats))
app.add_handler(MessageHandler(filters.TEXT,text))

print("AI TX BOT PRO RUNNING")

app.run_polling()
