from fastapi import FastAPI
from sqlalchemy.orm import Session

from database.db import SessionLocal
from database.models import Job

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/jobs")
def get_jobs():

    db: Session = SessionLocal()

    jobs = db.query(Job).all()

    result = []

    for job in jobs:
        result.append({
            "id": job.id,
            "title": job.title,
            "location": job.location,
            "url": job.link
        })

    db.close()

    return result