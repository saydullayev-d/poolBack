from pydantic import BaseModel, ConfigDict
from typing import Optional

class DiagnosisSchema(BaseModel):
    diagnosis_id: str
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
    
