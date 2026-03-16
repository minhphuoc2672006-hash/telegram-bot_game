import os
import base64
import zlib
import paho.mqtt.client as mqtt
import requests

# =========================
# ENV (không lộ token)
# =========================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

MQTT_HOST = os.getenv("MQTT_HOST", "broker.hivemq.com")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))

# =========================
# TELEGRAM
# =========================

def send_telegram(text):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass

# =========================
# HISTORY
# =========================

history = []

def analyze(total):

    history.append(total)

    if len(history) > 100:
        history.pop(0)

    tai = sum(1 for x in history if x >= 11)
    xiu = sum(1 for x in history if x <= 10)

    if tai > xiu:
        return "TÀI"
    else:
        return "XỈU"

# =========================
# DECODE PAYLOAD
# =========================

def decode_payload(payload):

    try:
        text = payload.decode("utf-8", errors="ignore")

        if len(text) < 20:
            return None

        data = base64.b64decode(text)

        try:
            data = zlib.decompress(data)
        except:
            pass

        return data.decode(errors="ignore")

    except:
        return None

# =========================
# MQTT EVENTS
# =========================

def on_connect(client, userdata, flags, rc):

    print("MQTT CONNECTED")

    client.subscribe("game/#")
    client.subscribe("taixiu/#")
    client.subscribe("tx/#")

    send_telegram("🤖 BOT ĐÃ KẾT NỐI SERVER")


def on_message(client, userdata, msg):

    print("TOPIC:", msg.topic)

    decoded = decode_payload(msg.payload)

    if decoded:

        print("DATA:", decoded)

        # Ví dụ parse xúc xắc
        if "dice" in decoded:

            try:

                numbers = [int(x) for x in decoded if x.isdigit()]

                if len(numbers) >= 3:

                    d1, d2, d3 = numbers[:3]

                    total = d1 + d2 + d3

                    prediction = analyze(total)

                    text = f"""
🎲 KẾT QUẢ

{d1} - {d2} - {d3}

Tổng: {total}

AI dự đoán ván sau:
{prediction}
"""

                    send_telegram(text)

            except:
                pass


def on_disconnect(client, userdata, rc):

    print("MQTT DISCONNECTED")


# =========================
# START BOT
# =========================

print("BOT STARTING...")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(MQTT_HOST, MQTT_PORT, 60)

client.loop_forever()
