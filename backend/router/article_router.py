from fastapi import APIRouter, HTTPException
from model.article_model import ValidateRequest, PublishArticle, UpdateArticle
from service.article_service.article_service import get_published_articles_service, get_scheduled_articles_service, get_unvalidated_articles_service, validate_article_service, update_article_service, get_article_service, delete_article_service, write_article_service

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    )

@router.post("/validate")
def validate_article(request: ValidateRequest):
    return validate_article_service(request.url, request.site_id, request.user_id, request.type)

@router.post("/write_article")
def write_article(article: PublishArticle):
    return write_article_service(article)


@router.put("/update_article")
def update_article(article: UpdateArticle):
    return update_article_service(article)

@router.get("/get_article/{id}")
def get_article(id: int):
    return get_article_service(id)

@router.delete("/delete_article/{id}")
def delete_article(id: int):
    return delete_article_service(id)

@router.get("/scheduled_articles/{site_id}")
def get_scheduled_articles(site_id: int):
    return get_scheduled_articles_service(site_id)

@router.get("/unvalidated_articles/{site_id}")
def get_unvalidated_articles(site_id: int):
    return get_unvalidated_articles_service(site_id)

@router.get("/get_published_articles/{site_id}")
def get_published_articles(site_id: int):
    return get_published_articles_service(site_id)