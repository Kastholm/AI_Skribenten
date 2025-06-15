from fastapi import APIRouter, HTTPException

from service.admin.admin_service import admin_get_all_users, admin_get_all_sites

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    )

@router.get("/all_users/{role}")
def get_all_users(role: str):
    return admin_get_all_users(role)

@router.get("/all_sites/{role}")
def get_all_sites(role: str):
    return admin_get_all_sites(role)