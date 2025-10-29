from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    password_repeat: str

class UserLogin(BaseModel):
    email: str
    password: str