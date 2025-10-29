from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Используем psycopg3
DATABASE_URL = "postgresql+psycopg://user:password@host:5432/dbname"

# Создаем движок
engine = create_engine(DATABASE_URL, future=True)

# Создаем сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс моделей
Base = declarative_base()

# Генератор сессий для зависимостей FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()