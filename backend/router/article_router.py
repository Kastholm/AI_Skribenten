from enum import Enum
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.article_service import get_scheduled_articles_service, get_unvalidated_articles_service, validate_article_service

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    )

class Article(BaseModel):
    site_id: int
    title: str
    teaser: str
    content: str
    img: str
    status: str
    response: str
    scheduled_publish_at: str
    published_at: str
    url: str
    prompt_instruction: str
    user_id: int
    category_id: int

""" @router.post("/add_article")
def add_article(article: Article):
    return add_article(article) """

@router.post("/validate/{url}")
def validate_article(url: str):
    return validate_article_service(url)

@router.get("/scheduled_articles/{site_id}")
def get_scheduled_articles(site_id: int):
    return get_scheduled_articles_service(site_id)

@router.get("/unvalidated_articles/{site_id}")
def get_unvalidated_articles(site_id: int):
    return get_unvalidated_articles_service(site_id)


