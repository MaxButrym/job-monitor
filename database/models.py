from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .db import Base


class Company(Base):
    """
    Модель компании.

    Описывает таблицу 'companies' в базе данных.
    Одна компания может иметь много вакансий (one-to-many).
    """

    __tablename__ = "companies"

    # Уникальный идентификатор компании
    id = Column(Integer, primary_key=True, index=True)

    # Название компании (уникальное, обязательное)
    name = Column(String(255), unique=True, nullable=False)

    # Рейтинг компании (например от 0 до 5)
    rating = Column(Float)

    # Связь с вакансиями
    jobs = relationship(
        "Job",
        back_populates="company",
        cascade="all, delete-orphan"
    )
    """
    cascade="all, delete-orphan":
    - при удалении компании удаляются все её вакансии
    - "осиротевшие" вакансии тоже удаляются
    """

    def __repr__(self):
        return f"<Company(id={self.id}, name={self.name})>"


class Job(Base):
    """
    Модель вакансии.

    Описывает таблицу 'jobs'.
    Каждая вакансия принадлежит одной компании.
    """

    __tablename__ = "jobs"

    # Уникальный идентификатор вакансии
    id = Column(Integer, primary_key=True, index=True)

    # Название вакансии (обязательное поле)
    title = Column(String(255), nullable=False)

    # Локация (город, страна и т.д.)
    location = Column(String(255), nullable=True)

    # Ссылка на вакансию
    link = Column(String(500), nullable=False)

    # Внешний ID вакансии (из сайта/API)
    # Используется для защиты от дублей
    external_id = Column(String(255), unique=True, index=True, nullable=False)

    # Внешний ключ на компанию
    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False,
        index=True
    )

    # Связь с компанией
    company = relationship("Company", back_populates="jobs")

    def __repr__(self):
        return f"<Job(id={self.id}, title={self.title})>"