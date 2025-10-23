from pydantic import BaseModel, ConfigDict

class GroupCreateSchema(BaseModel):
    name: str  # e.g., "Group A"
    
    model_config = ConfigDict(from_attributes=True)

class GroupResponseSchema(GroupCreateSchema):
    id: str
    model_config = ConfigDict(from_attributes=True)

    