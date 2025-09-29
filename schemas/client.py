from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import List, Optional

from .parent import ParentSchema
from .diagnosis_client import DiagnosisSchema
from .group_history import GroupHistorySchema
from .subscription import Subscription

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
    subscriptions: List[Subscription] = []
    photo: Optional[str] = None

class ClientResponseSchema(ClientCreateSchema):
    id: str
    birth_date: date
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
