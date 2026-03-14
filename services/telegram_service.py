import logging
from datetime import datetime
from telegram import Bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio



logging.basicConfig(level=logging.INFO)


TOKEN = "8723145759:AAESo6l1Ijvp634dVsm2O0dV-bn3imLN_mA"
CHAT_ID = "5687839275"


bot = Bot(token=TOKEN)


def send_job_notification(job):

    title = job["title"]
    company = job["company"]
    location = job["location"]
    rating = job["company_rating"]
    link = job["link"]

    if rating is None:
        rating = "нет данных"

    message = f"""
    ━━━━━━━━━━━━━━

    🚀 <b>Новая Python вакансия</b>

    💼 <b>{title}</b>

    🏢 Компания: <b>{company}</b>
    ⭐ Рейтинг: <b>{rating}</b>

    📍 Локация: <b>{location}</b>

    ━━━━━━━━━━━━━━
    """

    keyboard = [
        [
            InlineKeyboardButton(
                "🔎 Открыть вакансию",
                url=link
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    asyncio.run(
        bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
    )
    logging.info("Telegram уведомление о вакансии отправлено")




def send_parser_report(total, new, skipped):

    now = datetime.now().strftime("%H:%M")

    message = f"""
━━━━━━━━━━━━━━

🤖 <b>Проверка вакансий завершена</b>

🔎 Всего найдено: <b>{total}</b>
🆕 Новых вакансий: <b>{new}</b>
♻️ Дубликатов: <b>{skipped}</b>

⏰ Время проверки: <b>{now}</b>

━━━━━━━━━━━━━━
"""

    asyncio.run(
        bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode="HTML"
        )
    )
    logging.info("Telegram отчет парсера отправлен")