from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.site_service import create_site

router = APIRouter(
    prefix="/sites",
    tags=["sites"],
)

class Site(BaseModel):
    name: str
    logo: str
    page_url: str
    description: str

class LinkSite(BaseModel):
    user_id: int
    site_id: int


@router.post("/add_site")
def add_site(site: Site):
    result = create_site(site.name, site.logo, site.description, site.page_url)
    return result

@router.post("/link_site")
def link_site(link_site: LinkSite):
    result = link_site(link_site.user_id, link_site.site_id)
    return result
