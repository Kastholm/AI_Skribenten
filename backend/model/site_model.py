from enum import Enum
from pydantic import BaseModel


class Site(BaseModel):
    name: str
    logo: str
    page_url: str
    description: str

class SiteInfo(BaseModel):
    id: int
    name: str
    description: str
    page_url: str

class Role(str, Enum):
    viewer = "viewer"
    editor = "editor"

class LinkSite(BaseModel):
    user_id: int
    site_id: int
    role: Role