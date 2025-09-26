from pydantic import BaseModel

class ParentSchema(BaseModel):
    full_name: str
    phone: str
    relation_id: str
