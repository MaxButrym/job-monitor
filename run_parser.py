from parser.job_parser import parse_jobs
from services.job_service import save_jobs
from services.telegram_service import send_telegram_message


print("Запуск парсера...")
send_telegram_message("🚀 Парсер запущен")
jobs = parse_jobs()

print(f"Найдено вакансий: {len(jobs)}")

added = save_jobs(jobs)

if added > 0:
    send_telegram_message(f"🔥 Добавлено новых вакансий: {added}")
else:
    send_telegram_message("ℹ️ Новых вакансий по вашим фильтрам не найдено")

send_telegram_message(f"✅ Парсер завершил работу. Новых вакансий: {added}")