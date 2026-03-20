from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from typing import Optional

from database.db import SessionLocal
from database import models
from schemas.job import Job

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ ВАЖНО: response_model
@router.get("/jobs", response_model=list[Job])
def get_jobs(
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    sort_by: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    print("🔥 MY JOBS ENDPOINT WORKING")
    query = db.query(models.Job).options(joinedload(models.Job.company))

    if keyword:
        query = query.filter(models.Job.title.ilike(f"%{keyword}%"))

    if location:
        query = query.filter(models.Job.location.ilike(f"%{location}%"))
    
    if sort_by:
        if sort_by == "title":
            query = query.order_by(models.Job.title)
        elif sort_by == "location":
            query = query.order_by(models.Job.location)
        elif sort_by == "id":
            query = query.order_by(models.Job.id)    
        
        
    query = query.offset(offset).limit(limit)
    return query.all()


# ✅ исправлена скобка
@router.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: int, db: Session = Depends(get_db)):
    return db.query(models.Job).options(
        joinedload(models.Job.company)
    ).filter(models.Job.id == job_id).first()