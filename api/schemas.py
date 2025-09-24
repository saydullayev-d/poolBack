from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime
from typing import List, Optional

class RelationCreateSchema(BaseModel):
    name: str  # e.g., "Mother"

class RelationResponseSchema(RelationCreateSchema):
    id: str
    model_config = ConfigDict(from_attributes=True)

class DiagnosisCreateSchema(BaseModel):
    name: str  # e.g., "Scoliosis"

class DiagnosisResponseSchema(DiagnosisCreateSchema):
    id: str
    model_config = ConfigDict(from_attributes=True)

class GroupCreateSchema(BaseModel):
    name: str  # e.g., "Group A"

class GroupResponseSchema(GroupCreateSchema):
    id: str
    model_config = ConfigDict(from_attributes=True)

class SubscriptionTemplateCreateSchema(BaseModel):
    name: str  # e.g., "Monthly Plan"

class SubscriptionTemplateResponseSchema(SubscriptionTemplateCreateSchema):
    id: str
    model_config = ConfigDict(from_attributes=True)

class ParentSchema(BaseModel):
    full_name: str
    phone: str
    relation_id: str

class DiagnosisSchema(BaseModel):
    diagnosis_id: str
    notes: Optional[str] = None

class GroupHistorySchema(BaseModel):
    date: date
    action: str  # 'added' or 'removed'
    group_id: str

class RenewalHistorySchema(BaseModel):
    date: datetime = Field(default_factory=datetime.utcnow)
    from_template_id: Optional[str] = None
    to_template_id: str

class SubscriptionSchema(BaseModel):
    template_id: str
    start_date: date
    end_date: date
    classes_per_week: int = Field(..., ge=0, le=7)
    days_of_week: List[str] = []
    class_time: str
    group_id: Optional[str] = None
    remaining_classes: int
    is_paid: bool = True
    renewal_history: List[RenewalHistorySchema] = []
    subscription_number: str

class ClientCreateSchema(BaseModel):
    surname: str
    name: str
    patronymic: Optional[str] = None
    phone: str
    birth_date: date
    gender: str
    parents: List[ParentSchema] = []
    diagnoses: List[DiagnosisSchema] = []
    features: Optional[str] = None
    blacklisted: bool = False
    groups: List[str] = []
    group_history: List[GroupHistorySchema] = []
    subscriptions: List[SubscriptionSchema] = []
    photo: Optional[str] = None

class ClientResponseSchema(ClientCreateSchema):
    id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
