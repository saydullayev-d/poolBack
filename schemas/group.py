from pydantic import BaseModel, ConfigDict

class GroupCreateSchema(BaseModel):
    name: str  # e.g., "Group A"

class GroupResponseSchema(GroupCreateSchema):
    id: str
    model_config = ConfigDict(from_attributes=True)
