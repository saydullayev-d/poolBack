from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime
from typing import List, Optional

class RenewalHistorySchema(BaseModel):
    date: datetime = Field(default_factory=datetime.utcnow)
    from_template_id: Optional[str] = None
    to_template_id: str

class Payment(BaseModel):
    method: str  # "cash_register_cash", "cash_register_card", "cash", "bank_account"
    details: Optional[dict] = None
    date: datetime

class SubscriptionBase(BaseModel):
    template_id: str
    start_date: date
    end_date: date
    classes_per_week: int = Field(..., ge=0, le=7)
    days_of_week: List[str] = []
    class_time: str
    group: Optional[str] = None
    remaining_classes: int
    is_paid: bool = False
    subscription_number: str

class SubscriptionCreate(SubscriptionBase):
    payment: Optional[Payment] = None
    renewal_history: List[RenewalHistorySchema] = []

class Subscription(SubscriptionBase):
    id: str
    payment: Optional[Payment] = None
    renewal_history: List[RenewalHistorySchema] = []

    model_config = ConfigDict(from_attributes=True)


