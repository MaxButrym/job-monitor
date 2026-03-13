from database.db import engine, Base
from database import models

print("Создание таблиц...")

Base.metadata.create_all(bind=engine)

print("Таблицы созданы!")