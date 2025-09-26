from pydantic import BaseModel, ConfigDict

class DiagnosisCreateSchema(BaseModel):
    name: str  # e.g., "Scoliosis"

class DiagnosisResponseSchema(DiagnosisCreateSchema):
    id: str
    model_config = ConfigDict(from_attributes=True)
