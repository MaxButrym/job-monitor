from database.db import SessionLocal # Фабрика для создания сессий работы с базой данных
from database.models import Job, Company # ORM модели таблиц: вакансии и компании
from sqlalchemy.exc import IntegrityError


def save_jobs(jobs):
    db = SessionLocal()

    saved = 0
    skipped = 0
    new_jobs = []
    total = len(jobs)

    for job_data in jobs:
        print(f"🔍 Проверяю: {job_data['title']}")

        # 1. проверка / создание компании
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

        # 2. проверка дубликата
        existing_job = db.query(Job).filter(
            Job.external_id == job_data["external_id"]
        ).first()

        if existing_job:
            print(f"⏭️ Пропуск (дубликат): {job_data['title']}")
            skipped += 1
            continue

        # 3. создание вакансии
        job = Job(
            title=job_data["title"],
            location=job_data["location"],
            link=job_data["link"],
            external_id=job_data["external_id"],
            company_id=company.id
        )

        try:
            db.add(job)
            db.commit()

            print(f"✅ Добавляю: {job_data['title']}")

            new_jobs.append(job_data)
            saved += 1

        except IntegrityError:
            db.rollback()
            skipped += 1

    db.close()

    return total, saved, skipped, new_jobs