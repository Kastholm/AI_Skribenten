from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.user_service import admin_get_all_users, create_user, get_user_sites_service, login_user

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

@router.get("/info")
def get_user_info():
    result = admin_get_all_users()
    return result

@router.post("/register")
def register(user: User):
    create_user(user.name, user.username, user.password)
    return {"message": "User registered successfully", "user": user}

@router.post("/login")
def login(user: LoginUser):
    result = login_user(user.username, user.password)
    return result

@router.get("/sites/{user_id}")
def get_user_sites(user_id: int):
    return get_user_sites_service(user_id)