from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from config.database import Session
from utils.jwt_manager import create_token
from models.user import User as User_model
from schemas.user import User

user_router = APIRouter()

@user_router.post('/login', tags=['auth'])
def login(user: User):
    userEmail = get_user_by_email(user.email)
    if not userEmail:
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials - User Incorrect"})
    token: str = create_token(user.model_dump())
    return JSONResponse(status_code=200, content=token)

def get_user_by_email(email: str):
    db = Session()
    result = db.query(User_model).filter(User_model.email == email).first()
    return result