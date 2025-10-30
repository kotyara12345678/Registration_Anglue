import os
from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.Auth_core.Auth_database import get_db, Base, engine
from app.Auth_work.auth import AuthManager
from app.Auth_schemas.schemas import UserCreate, UserLogin

Base.metadata.create_all(bind=engine)

app = FastAPI()
auth = AuthManager()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/protected", response_class=HTMLResponse)
async def protected_page(request: Request, user=Depends(auth.auth_required)):
    return templates.TemplateResponse("protected.html", {"request": request, "user": user})


@app.post("/register")
async def register(data: UserCreate, db: Session = Depends(get_db)):
    if data.password != data.password_repeat:
        raise HTTPException(status_code=400, detail="Пароли не совпадают")
    user = auth.register(db, data.email, data.password)
    return {"message": "Регистрация успешна", "email": user.email}


@app.post("/login")
async def login(data: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = auth.login(db, response, data.email, data.password)
    return {"message": "Вход успешен", "email": user.email}


@app.post("/logout")
async def logout(response: Response):
    auth.logout(response)
    return {"message": "Вы вышли"}


@app.get("/api/protected")
async def protected_api(user=Depends(auth.auth_required)):
    return {"message": f"Добро пожаловать, {user['uid']}!"}