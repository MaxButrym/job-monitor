import schedule
import time

from parser.job_parser import parse_jobs
from services.job_service import save_jobs


def job():

    print("Запуск парсера...")

    jobs = parse_jobs()

    print(f"Найдено вакансий: {len(jobs)}")

    save_jobs(jobs)


print("Scheduler запущен...")

job()

schedule.every(30).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)