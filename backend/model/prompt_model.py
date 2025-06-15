from pydantic import BaseModel


class Prompt(BaseModel):
    name: str
    description: str
    user_id: int
