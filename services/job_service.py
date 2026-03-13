from database.db import SessionLocal
from database.models import Job


def save_jobs(jobs):

    db = SessionLocal()

    for job_data in jobs:

        job = Job(title=job_data["title"])

        db.add(job)

    db.commit()

    db.close()