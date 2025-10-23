from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import List, Optional
from .subscription import Subscription

class ContractBase(BaseModel):
    creation_date: date

class ContractCreate(ContractBase):
    subscriptions: List[Subscription] = []

class Contract(ContractBase):
    id: str
    subscriptions: List[Subscription] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
