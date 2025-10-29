from fastapi import FastAPI, HTTPException, Depends
from authx import AuthX, AuthXConfig
from app.Auth_schemas.schemas import UserLoginSchema

app = FastAPI()


config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

@app.post("/login")
async def login(creds: UserLoginSchema):

    if creds.username == "test" and creds.password == "test":

        access_token = security.create_access_token(subject=creds.username)

        response = {"access_token": access_token}
        security.set_access_cookie(response, access_token)
        return response

    raise HTTPException(status_code=401, detail="Неверный логин или пароль")

@app.get("/protected")
async def protected(user=Depends(security.access_token_required)):
    return {"message": f"Добро пожаловать, {user['sub']}!"}