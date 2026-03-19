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

@app.get("/")
def root():
    return {"message": "job-monitor API работает"}

from typing import Optional
from fastapi import Query

@app.get("/jobs")
def get_jobs(
    keyword: Optional[str] = Query(None),
    location: Optional[str] = Query(None)
):
    db: Session = SessionLocal()

    query = db.query(Job)

    if keyword:
        query = query.filter(Job.title.ilike(f"%{keyword}%"))

    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))

    jobs = query.all()

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

@app.get("/jobs/{job_id}")
def get_job(job_id: int):

    db: Session = SessionLocal()

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        db.close()
        return {"error": "Job not found"}

    result = {
        "id": job.id,
        "title": job.title,
        "location": job.location,
        "url": job.link
    }

    db.close()

    return result