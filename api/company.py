from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from database import models
from schemas.company import Company, CompanyWithJobs


# создаем роутер для компаний
router = APIRouter(
    prefix="/companies",   # все маршруты будут начинаться с /companies
    tags=["Companies"]     # группа в swagger
)


# -------------------------
# получить список компаний
# -------------------------
@router.get("/", response_model=list[Company])
def get_companies(db: Session = Depends(get_db)):
    # берем все компании из базы
    # сортируем по id (сначала новые)
    companies = db.query(models.Company)\
        .order_by(models.Company.id.desc())\
        .all()

    # возвращаем список компаний
    return companies


# -------------------------
# получить одну компанию по id
# -------------------------
@router.get("/{company_id}", response_model=CompanyWithJobs)
def get_company(company_id: int, db: Session = Depends(get_db)):
    # ищем компанию по id
    company = db.query(models.Company).filter(
        models.Company.id == company_id
    ).first()

    # если не нашли — ошибка 404
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # возвращаем компанию (вместе с вакансиями)
    return company