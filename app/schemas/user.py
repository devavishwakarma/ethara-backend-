from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "member"    