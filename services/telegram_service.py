import logging
from datetime import datetime
from telegram import Bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import TELEGRAM_TOKEN


logging.basicConfig(level=logging.INFO)


CHAT_ID = "5687839275"


bot = Bot(token=TELEGRAM_TOKEN)


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

    bot.send_message(
        chat_id=CHAT_ID,
        text=message,
        parse_mode="HTML",
        reply_markup=reply_markup
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


    bot.send_message(
        chat_id=CHAT_ID,
        text=message,
        parse_mode="HTML"
    )
    logging.info("Telegram отчет парсера отправлен")
    
async def send_jobs_summary(jobs):
    message = "🔥 Найдено новых вакансий:\n\n"

    for i, job in enumerate(jobs[:10], 1):  # ограничим 10
        message += f"{i}. {job['title']} — {job['location']}\n"

    if len(jobs) > 10:
        message += f"\n...и ещё {len(jobs) - 10}"

    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )
async def send_no_jobs_message():
    await bot.send_message(
        chat_id=CHAT_ID,
        text="❌ Новых вакансий нет"
    )