from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import List, Optional

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
