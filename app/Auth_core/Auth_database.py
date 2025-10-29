from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Используем имя сервиса 'db' как хост
DATABASE_URL = "postgresql+psycopg://postgres:postgres@db:5432/postgres"

engine = create_engine(DATABASE_URL, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()