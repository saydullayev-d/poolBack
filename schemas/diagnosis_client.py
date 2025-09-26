from pydantic import BaseModel
from typing import Optional

class DiagnosisSchema(BaseModel):
    diagnosis_id: str
    notes: Optional[str] = None
