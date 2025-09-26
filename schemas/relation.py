from pydantic import BaseModel, ConfigDict

class RelationCreateSchema(BaseModel):
    name: str  # e.g., "Mother"

class RelationResponseSchema(RelationCreateSchema):
    id: str
    model_config = ConfigDict(from_attributes=True)
