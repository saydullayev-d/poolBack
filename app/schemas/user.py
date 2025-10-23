from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    name: str
    password: str
    role: str

class UserCreate(UserBase):
    pass

class UsersResponse(UserBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
