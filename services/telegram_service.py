import logging
from datetime import datetime
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


# создаем логгер для этого файла
logger = logging.getLogger(__name__)

# создаем бота с токеном
bot = Bot(token=TELEGRAM_TOKEN)


# -------------------------
# отправить одну вакансию в телеграм
# -------------------------
def send_job_notification(job):
    try:
        # достаем данные из словаря вакансии
        title = job["title"]
        company = job["company"]
        location = job["location"]
        rating = job["company_rating"]
        link = job["link"]

        # если рейтинг None — подставляем текст
        if rating is None:
            rating = "нет данных"

        # формируем сообщение (html разметка для жирного текста)
        message = f"""
━━━━━━━━━━━━━━

🚀 <b>Новая Python вакансия</b>

💼 <b>{title}</b>

🏢 Компания: <b>{company}</b>
⭐ Рейтинг: <b>{rating}</b>

📍 Локация: <b>{location}</b>

━━━━━━━━━━━━━━
"""

        # создаем кнопку с ссылкой на вакансию
        keyboard = [
            [InlineKeyboardButton("🔎 Открыть вакансию", url=link)]
        ]

        # оборачиваем кнопку в markup
        reply_markup = InlineKeyboardMarkup(keyboard)

        # отправляем сообщение в телеграм
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode="HTML",  # чтобы работал <b>
            reply_markup=reply_markup
        )

        # лог что все ок
        logger.info("Отправлено уведомление о вакансии")

    except Exception:
        # логируем ошибку (exc_info=True покажет traceback)
        logger.error("Ошибка отправки вакансии в Telegram", exc_info=True)


# -------------------------
# отправить отчет парсера
# -------------------------
def send_parser_report(total, new, skipped):
    try:
        # текущее время (для отчета)
        now = datetime.now().strftime("%H:%M")

        # формируем сообщение
        message = f"""
━━━━━━━━━━━━━━

🤖 <b>Проверка вакансий завершена</b>

🔎 Всего найдено: <b>{total}</b>
🆕 Новых вакансий: <b>{new}</b>
♻️ Дубликатов: <b>{skipped}</b>

⏰ Время проверки: <b>{now}</b>

━━━━━━━━━━━━━━
"""

        # отправляем сообщение
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode="HTML"
        )

        # лог успеха
        logger.info("Отправлен отчет парсера")

    except Exception:
        # лог ошибки
        logger.error("Ошибка отправки отчета", exc_info=True)


# -------------------------
# отправить краткий список вакансий
# -------------------------
def send_jobs_summary(jobs):
    try:
        # начало сообщения
        message = "🔥 Найдено новых вакансий:\n\n"

        # берем максимум 10 вакансий
        for i, job in enumerate(jobs[:10], 1):
            message += f"{i}. {job['title']} — {job['location']}\n"

        # если вакансий больше 10 — дописываем
        if len(jobs) > 10:
            message += f"\n...и ещё {len(jobs) - 10}"

        # отправляем сообщение
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )

        # лог успеха
        logger.info("Отправлен summary вакансий")

    except Exception:
        # лог ошибки
        logger.error("Ошибка отправки summary", exc_info=True)


# -------------------------
# отправить сообщение что вакансий нет
# -------------------------
def send_no_jobs_message():
    try:
        # отправляем простое сообщение
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text="❌ Новых вакансий нет"
        )

        # лог
        logger.info("Отправлено сообщение: вакансий нет")

    except Exception:
        # лог ошибки
        logger.error("Ошибка отправки сообщения 'нет вакансий'", exc_info=True)


# -------------------------
# отправить сообщение об ошибке
# -------------------------
def send_error_message(error_text: str):
    try:
        # формируем сообщение с текстом ошибки
        message = f"❌ Ошибка в парсере:\n{error_text}"

        # отправляем
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )

        # лог (тут используем error, т.к. это реально ошибка)
        logger.error("Отправлено сообщение об ошибке")

    except Exception:
        # если даже это упало — логируем
        logger.error("Ошибка отправки ошибки в Telegram", exc_info=True)