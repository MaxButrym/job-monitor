from database.db import SessionLocal
from database.models import Job, Company
from sqlalchemy.exc import IntegrityError
from services.telegram_service import send_job_notification, send_parser_report

import time


def save_jobs(jobs):

    db = SessionLocal()

    saved = 0
    skipped = 0

    for job_data in jobs:

        company = db.query(Company).filter(
            Company.name == job_data["company"]
        ).first()

        if not company:

            company = Company(
                name=job_data["company"],
                rating=job_data["company_rating"]
            )

            db.add(company)
            db.commit()
            db.refresh(company)

        job = Job(
            title=job_data["title"],
            location=job_data["location"],
            link=job_data["link"],
            company_id=company.id
        )

        try:

            db.add(job)
            db.commit()

            send_job_notification(job_data)

            time.sleep(1)

            saved += 1

        except IntegrityError:

            db.rollback()

            skipped += 1

    db.close()

    total = saved + skipped

    print(f"Добавлено вакансий: {saved}")
    print(f"Пропущено (дубликаты): {skipped}")

    send_parser_report(total, saved, skipped)