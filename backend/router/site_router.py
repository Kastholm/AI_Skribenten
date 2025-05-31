from enum import Enum
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.site_service import admin_get_all_sites, admin_link_site_service, create_site

router = APIRouter(
    prefix="/sites",
    tags=["sites"],
)

class Site(BaseModel):
    name: str
    logo: str
    page_url: str
    description: str

class Role(str, Enum):
    viewer = "viewer"
    editor = "editor"

class LinkSite(BaseModel):
    user_id: int
    site_id: int
    role: Role

@router.get("/all")
def get_all_sites():
    result = admin_get_all_sites()
    return result

@router.post("/add_site")
def add_site(site: Site):
    result = create_site(site.name, site.logo, site.description, site.page_url)
    return result

@router.post("/link_site")
def link_site(link_site: LinkSite):
    result = admin_link_site_service(link_site.user_id, link_site.site_id, link_site.role)
    return result
