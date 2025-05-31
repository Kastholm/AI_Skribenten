from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.user_service import create_user, login_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

class User(BaseModel):
    name: str
    username: str
    password: str

class LoginUser(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: User):
    create_user(user.name, user.username, user.password)
    return {"message": "User registered successfully", "user": user}

@router.post("/login")
def login(user: LoginUser):
    result = login_user(user.username, user.password)
    return result
