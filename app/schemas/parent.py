from pydantic import BaseModel, ConfigDict

class ParentSchema(BaseModel):
    full_name: str
    phone: str
    relation_id: str
    
    model_config = ConfigDict(from_attributes=True)
