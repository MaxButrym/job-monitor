from database.db import SessionLocal # Фабрика для создания сессий работы с базой данных
from database.models import Job, Company # ORM модели таблиц: вакансии и компании
from sqlalchemy.exc import IntegrityError # Ошибка целостности БД (например, при попытке добавить дубликат)

# Сохраняет список вакансий в базу данных:
# - создает компании при необходимости
# - пропускает дубликаты
# - возвращает статистику
def save_jobs(jobs):
    # Создаем сессию для работы с БД
    db = SessionLocal()
    
    # Счетчики для статистики
    saved = 0  # успешно добавленные вакансии
    skipped = 0 # пропущенные (дубликаты/ошибки)
    new_jobs = [] # список новых вакансий
    total = len(jobs) # общее количество полученных вакансий

    # Обрабатываем каждую вакансию из списка
    for job_data in jobs:
        print(f"🔍 Проверяю: {job_data['title']}") # Логируем текущую вакансию

        # --- 1. Проверка существования компании ---
        # Ищем компанию по имени
        company = db.query(Company).filter(
            Company.name == job_data["company"]
        ).first()
        # Если компании нет — создаем новую
        if not company:
            company = Company(
                name=job_data["company"],
                rating=job_data["company_rating"]
            )
            db.add(company) # добавляем в сессию
            db.commit() # сохраняем в БД
            db.refresh(company) # обновляем объект (получаем id)

        # --- 2. Проверка на дубликат вакансии ---
        # Ищем вакансию по внешнему ID (уникальный идентификатор)
        existing_job = db.query(Job).filter(
            Job.external_id == job_data["external_id"]
        ).first()
        # Если вакансия уже есть — пропускаем
        if existing_job:
            print(f"⏭️ Пропуск (дубликат): {job_data['title']}")
            skipped += 1
            continue

        # --- 3. Создание новой вакансии ---
        # Формируем объект вакансии
        job = Job(
            title=job_data["title"],
            location=job_data["location"],
            link=job_data["link"],
            external_id=job_data["external_id"],
            company_id=company.id
        )
        # Пытаемся сохранить вакансию в БД
        try:
            db.add(job) # добавляем в сессию
            db.commit() # сохраняем

            print(f"✅ Добавляю: {job_data['title']}") # сохраняем в список новых

            new_jobs.append(job_data)
            saved += 1

        except IntegrityError:
            # В случае ошибки (например, нарушение уникальности)
            db.rollback() # откатываем изменения
            print (f"⚠️ Уже существует: {job_data['title']} ")
            skipped += 1
    # Закрываем сессию БД
    db.close()
    # Возвращаем статистику обработки
    return total, saved, skipped, new_jobs