from database.db import SessionLocal
from database.models import Job
from sqlalchemy.exc import IntegrityError


def save_jobs(jobs):

    db = SessionLocal()

    saved = 0
    skipped = 0

    for job_data in jobs:

        job = Job(
            title=job_data["title"]
        )

        try:
            db.add(job)
            db.commit()
            saved += 1

        except IntegrityError:
            db.rollback()
            skipped += 1

    db.close()

    print(f"Добавлено: {saved}")
    print(f"Пропущено (дубликаты): {skipped}")