from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import SessionLocal
from database import models
from schemas.company import Company, CompanyWithJobs

router = APIRouter()


# -------------------------
# Dependency (подключение к БД)
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# GET /companies
# -------------------------
@router.get("/companies", response_model=list[Company])
def get_companies(db: Session = Depends(get_db)):
    companies = db.query(models.Company).all()
    return companies


# -------------------------
# GET /companies/{id}
# -------------------------
@router.get("/companies/{company_id}", response_model=CompanyWithJobs)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(
        models.Company.id == company_id
    ).first()

    return company