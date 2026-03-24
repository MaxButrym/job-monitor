from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

# ENGINE — это "ядро" подключения к базе данных
# Он знает КУДА подключаться и управляет соединениями
engine = create_engine(
    DATABASE_URL,
    # Проверяет соединение перед использованием
    # Если соединение "умерло" — автоматически пересоздаст
    pool_pre_ping=True
)
# SessionLocal — это ФАБРИКА сессий (не сама сессия!)
# Каждый вызов SessionLocal() создаёт новую сессию (db)
SessionLocal = sessionmaker(
    # Автоматический commit выключен
    # ты сам контролируешь, когда сохранять изменения
    autocommit=False,
    # Автоматическая отправка запросов в БД выключена
    # SQLAlchemy не будет сам "флашить" изменения
    autoflush=False,
    # Привязываем сессии к нашему engine (подключению)
    bind=engine
)
# Base — базовый класс для всех ORM моделей
# Все модели должны наследоваться от него
Base = declarative_base()


def get_db():
    """
    Dependency для FastAPI

    Используется так:
    db: Session = Depends(get_db)

    Что делает:
    1. Создаёт сессию
    2. Отдаёт её в endpoint
    3. Гарантированно закрывает после использования
    """
    # Создаём новую сессию
    db = SessionLocal()
    try:
        # Передаём сессию в FastAPI endpoint
        yield db
    finally:
        # ОБЯЗАТЕЛЬНО закрываем соединение
        # защищает от утечек подключений
        db.close()


def get_db_session():
    """
    Используется вне FastAPI (например в run_parser)

    ВАЖНО:
    👉 здесь ты САМ должен закрыть сессию!
    """
    return SessionLocal()