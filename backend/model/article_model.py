from pydantic import BaseModel


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

class UpdateArticle(BaseModel):
    id: int
    title: str
    url: str
    content: str
    img: str
    prompt_instruction: str
    instructions: str
    scheduled_publish_at: str
    user_id: int
    teaser: str

class PublishArticle(BaseModel):
    id: int
    site_id: int
    title: str
    teaser: str
    content: str
    img: str
    prompt_instructions: str
    instructions: str
    user_id: int

class ValidateRequest(BaseModel):
    url: str
    type: str
    site_id: int
    user_id: int