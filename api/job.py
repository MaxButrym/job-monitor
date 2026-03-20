from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload

from typing import Optional
from database.db import SessionLocal
from database import models
from schemas.job import Job, JobList, JobListResponse


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ ВАЖНО: response_model
@router.get("/jobs", response_model=JobListResponse)
def get_jobs(
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    company: Optional[str] = None,
    sort_by: Optional[str] = None,
    limit: int = Query(10, ge=1, le=50),
    offset: int = 0,
    db: Session = Depends(get_db)
):

    query = db.query(models.Job).join(models.Job.company).options(joinedload(models.Job.company))
    
    if keyword:
        query = query.filter(models.Job.title.ilike(f"%{keyword}%"))

    if location:
        query = query.filter(models.Job.location.ilike(f"%{location}%"))
    
    if company:
        query = query.filter(models.Company.name.ilike(f"%{company}%"))
    
    if sort_by:
        desc = sort_by.startswith("-")
        field = sort_by.lstrip("-")
        
        if field == "title":
            column = models.Job.title
        elif field == "location":
            column = models.Job.location
        elif field == "id":
            column = models.Job.id
        else:
            column = None   
            
        if column is not None:
            if desc:
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column)
        
        
    query = query.offset(offset).limit(limit)
    total = query.count()
    
    jobs = query.offset(offset).limit(limit).all()
    
    return {
        "total": total,
        "items": jobs
    }


# ✅ исправлена скобка
@router.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: int, db: Session = Depends(get_db)):
    return db.query(models.Job).options(
        joinedload(models.Job.company)
    ).filter(models.Job.id == job_id).first()