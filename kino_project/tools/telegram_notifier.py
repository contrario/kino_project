# kino_project/tools/telegram_notifier.py

import requests

BOT_TOKEN = "8393168645:AAG-acWe2Kdw_JXYPQ3ZvNYaBrb64lgivPA"
CHAT_ID = "6046304883"

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except Exception as e:
        print(f"[Telegram] Error sending message: {e}")
