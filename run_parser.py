import logging
from core.logging_config import setup_logging

from parser.job_parser import parse_jobs
from services.job_service import save_jobs
from services.telegram_service import (
    send_jobs_summary,
    send_no_jobs_message,
    send_parser_report
)


setup_logging()
logger = logging.getLogger(__name__)


def main():
    logger.info("🚀 Запуск парсера...")

    # 1. парсинг
    jobs = parse_jobs()
    logger.info(f"Найдено вакансий: {len(jobs)}")

    # 2. сохранение
    total, saved, skipped, new_jobs = save_jobs(jobs)

    logger.info(f"Добавлено: {saved}")
    logger.info(f"Пропущено: {skipped}")

    # 3. Telegram
    if new_jobs:
        send_jobs_summary(new_jobs)
    else:
        send_no_jobs_message()

    # 4. отчет
    send_parser_report(total, saved, skipped)


if __name__ == "__main__":
    main()