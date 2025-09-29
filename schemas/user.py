from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    password: str
    role: str  # например: "admin", "manager", "trainer"

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str

    class Config:
        from_attributes = True
