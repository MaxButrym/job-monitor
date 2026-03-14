from telegram import Bot
import requests


TOKEN = "8723145759:AAESo6l1Ijvp634dVsm2O0dV-bn3imLN_mA"
CHAT_ID = "5687839275"


bot = Bot(token=TOKEN)


def send_job_notification(job):

    message = f"""
Новая вакансия

{job["title"]}

Компания: {job["company"]}
Локация: {job["location"]}

{job["link"]}
"""

    bot.send_message(chat_id=CHAT_ID, text=message)


def send_telegram_message(text):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    response = requests.post(url, json=data)

    return response.json()