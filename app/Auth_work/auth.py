from fastapi import Response, HTTPException, Depends
from sqlalchemy.orm import Session
from authx import AuthX, AuthXConfig
from app.Auth_models.models import User
from app.Auth_core.Auth_database import get_db

class AuthManager:
    def init(self):
        config = AuthXConfig()
        config.JWT_SECRET_KEY = "SECRET_KEY"
        config.JWT_ACCESS_COOKIE_NAME = "access_token"
        config.JWT_TOKEN_LOCATION = ["cookies"]
        self.security = AuthX(config=config)

    def register(self, db: Session, email: str, password: str):
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email уже используется")
        user = User(email=email, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def login(self, db: Session, response: Response, email: str, password: str):
        user = db.query(User).filter(User.email == email, User.password == password).first()
        if not user:
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")
        token = self.security.create_access_token(uid=user.email)
        self.security.set_access_cookies(response=response, token=token)
        return user

    def logout(self, response: Response):
        self.security.unset_cookies(response=response)

    def auth_required(self, user=Depends(AuthX(config=AuthXConfig()).access_token_required)):
        return user