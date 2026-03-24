from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload

from typing import Optional
from database.db import get_db
from database import models
from schemas.job import Job, JobListResponse


# создаем роутер для вакансий
router = APIRouter(
    prefix="/jobs",   # все маршруты начинаются с /jobs
    tags=["Jobs"]     # группа в swagger
)


# -------------------------
# получить список вакансий с фильтрами
# -------------------------
@router.get("/", response_model=JobListResponse)
def get_jobs(
    keyword: Optional[str] = None,   # поиск по названию вакансии
    location: Optional[str] = None,  # фильтр по локации
    company: Optional[str] = None,   # фильтр по компании
    sort_by: Optional[str] = None,   # сортировка (например: title или -id)
    limit: int = Query(10, ge=1, le=50),  # сколько вернуть (от 1 до 50)
    offset: int = 0,  # с какого места начинать (для пагинации)
    db: Session = Depends(get_db)
):

    # создаем базовый запрос
    # join нужен чтобы можно было фильтровать по компании
    # joinedload — чтобы сразу подтянуть компанию (без доп. запросов)
    query = db.query(models.Job)\
        .join(models.Job.company)\
        .options(joinedload(models.Job.company))
    
    # фильтр по ключевому слову (в названии вакансии)
    if keyword:
        query = query.filter(models.Job.title.ilike(f"%{keyword}%"))

    # фильтр по локации
    if location:
        query = query.filter(models.Job.location.ilike(f"%{location}%"))
    
    # фильтр по названию компании
    if company:
        query = query.filter(models.Company.name.ilike(f"%{company}%"))
    
    # сортировка
    if sort_by:
        # если начинается с "-" → значит сортировка по убыванию
        desc = sort_by.startswith("-")

        # убираем "-" чтобы понять поле
        field = sort_by.lstrip("-")
        
        # выбираем колонку для сортировки
        if field == "title":
            column = models.Job.title
        elif field == "location":
            column = models.Job.location
        elif field == "id":
            column = models.Job.id
        else:
            column = None   
            
        # если поле норм — применяем сортировку
        if column is not None:
            query = query.order_by(column.desc() if desc else column)
    
    # считаем общее количество (для фронта / пагинации)
    total = query.count()
    
    # применяем пагинацию (offset + limit)
    jobs = query.offset(offset).limit(limit).all()
    
    # возвращаем результат
    return {
        "total": total,
        "items": jobs
    }


# -------------------------
# получить одну вакансию по id
# -------------------------
@router.get("/{job_id}", response_model=Job)
def get_job(job_id: int, db: Session = Depends(get_db)):
    
    # ищем вакансию + сразу подтягиваем компанию
    job = db.query(models.Job)\
        .options(joinedload(models.Job.company))\
        .filter(models.Job.id == job_id)\
        .first()
    
    # если не нашли — ошибка 404
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # возвращаем вакансию
    return job