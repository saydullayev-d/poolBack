from pydantic import BaseModel, ConfigDict

class SubscriptionTemplateCreateSchema(BaseModel):
    name: str  # e.g., "Monthly Plan"

class SubscriptionTemplateResponseSchema(SubscriptionTemplateCreateSchema):
    id: str
    model_config = ConfigDict(from_attributes=True)
