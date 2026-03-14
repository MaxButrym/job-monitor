import database.models  # noqa: F401
from database.db import engine, Base

print("Создание таблиц...")

Base.metadata.create_all(engine)

print("Таблицы успешно созданы!")