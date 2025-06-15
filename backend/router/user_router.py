from fastapi import APIRouter, HTTPException
from service.user_service import create_user, get_user_sites_service, login_user
from model.user_model import User, LoginUser

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/register")
def register(user: User):
    return create_user(user.name, user.username, user.password)

@router.post("/login")
def login(user: LoginUser):
    return login_user(user.username, user.password)

@router.get("/sites/{user_id}")
def get_user_sites(user_id: int):
    return get_user_sites_service(user_id)