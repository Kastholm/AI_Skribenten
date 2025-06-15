from fastapi import APIRouter, HTTPException
from service.site_service import link_site_service, create_site, get_site_by_id_service, update_site_service
from model.site_model import Site, SiteInfo, LinkSite

router = APIRouter(
    prefix="/sites",
    tags=["sites"],
)

@router.post("/add_site")
def add_site(site: Site):
    return create_site(site.name, site.logo, site.description, site.page_url)

@router.post("/link_site")
def link_site(link_site: LinkSite):
    return link_site_service(link_site.user_id, link_site.site_id, link_site.role)

@router.get("/get_site_by_id/{site_id}")
def get_site_by_id(site_id: int):
    return get_site_by_id_service(site_id)

@router.put("/update_site/{site_id}")
def update_site(site_id: int, site: Site):
    return update_site_service(site_id, site.name, site.logo, site.description, site.page_url)