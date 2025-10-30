from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles
from app.Auth_core.Auth_database import get_db, Base, engine
from app.Auth_work.auth import AuthManager
from app.Auth_schemas.schemas import UserCreate, UserLogin
from fastapi.templating import Jinja2Templates

Base.metadata.create_all(bind=engine)

app = FastAPI()
auth = AuthManager()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

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

@app.get("/protected")
async def protected(user=Depends(auth.auth_required)):
    return {"message": f"Добро пожаловать, {user['uid']}!"}