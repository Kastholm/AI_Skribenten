from enum import Enum
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.prompt_service import get_all_prompts, create_prompt

router = APIRouter(
    prefix="/prompts",
    tags=["prompts"],
    )

class Prompt(BaseModel):
    name: str
    description: str
    user_id: int


@router.post("/create")
def create_prompt_route(prompt: Prompt):
    return create_prompt(prompt.name, prompt.description, prompt.user_id)

@router.get("/all/{user_id}")
def get_all_prompts_route(user_id: int):
    return get_all_prompts(user_id)
