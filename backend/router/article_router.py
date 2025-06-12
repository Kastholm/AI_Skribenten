from enum import Enum
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.article_service.article_service import get_scheduled_articles_service, get_unvalidated_articles_service, validate_article_service, update_article_service, get_article_service, delete_article_service

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    )

class FullArticle(BaseModel):
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
    instructions: str
    prompt_instruction: str
    user_id: int
    category_id: int

class UpdateArticle(BaseModel):
    id: int
    title: str
    url: str
    content: str
    img: str
    prompt_instruction: str
    instructions: str
    scheduled_publish_at: str
    category_id: int
    user_id: int
    teaser: str

class ValidateRequest(BaseModel):
    url: str
    site_id: int
    user_id: int


@router.post("/validate")
def validate_article(request: ValidateRequest):
    return validate_article_service(request.url, request.site_id, request.user_id)


@router.put("/update_article")
def update_article(article: UpdateArticle):
    return update_article_service(article)

@router.get("/get_article/{id}")
def get_article(id: int):
    return get_article_service(id)

@router.delete("/delete_article/{id}")
def delete_article(id: int):
    return delete_article_service(id)

""" @router.post("/add_article")
def add_article(article: Article):
    return add_article(article) """

@router.get("/scheduled_articles/{site_id}")
def get_scheduled_articles(site_id: int):
    return get_scheduled_articles_service(site_id)

@router.get("/unvalidated_articles/{site_id}")
def get_unvalidated_articles(site_id: int):
    return get_unvalidated_articles_service(site_id)