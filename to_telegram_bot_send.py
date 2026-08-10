import requests
import os

def send_telegram(text: str):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    
    # Telegram лимит 4096 символов на сообщение — режь на чанки
    for chunk in split_message(text, 4000):
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": chunk, "parse_mode": "Markdown"}
        )
