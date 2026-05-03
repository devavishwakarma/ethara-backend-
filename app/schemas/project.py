from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str
    user_id: int