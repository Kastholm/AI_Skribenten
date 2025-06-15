from fastapi import APIRouter, HTTPException
from model.prompt_model import Prompt
from service.prompt_service import get_all_prompts, create_prompt, delete_user_prompt_service, update_user_prompt_service

router = APIRouter(
    prefix="/prompts",
    tags=["prompts"],
    )

@router.post("/create")
def create_prompt_route(prompt: Prompt):
    return create_prompt(prompt.name, prompt.description, prompt.user_id)

@router.get("/all/{user_id}")
def get_all_prompts_route(user_id: int):
    return get_all_prompts(user_id)

@router.delete("/delete/{prompt_id}/{user_id}")
def delete_prompt_route(prompt_id: int, user_id: int):
    return delete_user_prompt_service(prompt_id, user_id)

@router.put("/update/{prompt_id}/{user_id}")
def update_prompt_route(prompt_id: int, user_id: int, prompt_data: dict):
    return update_user_prompt_service(prompt_id, prompt_data["name"], prompt_data["description"], user_id)
