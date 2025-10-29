from sqlalchemy import Column, Integer, String
from app.Auth_core.Auth_database import Base

class User(Base):
    tablename = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)