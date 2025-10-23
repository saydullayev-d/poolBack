from pydantic import BaseModel, ConfigDict

class RelationCreateSchema(BaseModel):
    name: str  # e.g., "Mother"
    
    model_config = ConfigDict(from_attributes=True)

class RelationResponseSchema(RelationCreateSchema):
    id: str
    model_config = ConfigDict(from_attributes=True)
    

