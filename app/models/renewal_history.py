import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from .base import Base

class RenewalHistory(Base):
    __tablename__ = "renewal_histories"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    subscription_id = Column(String, ForeignKey("subscriptions.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    from_template_id = Column(String, ForeignKey("subscription_templates.id"), nullable=True)
    to_template_id = Column(String, ForeignKey("subscription_templates.id"), nullable=False)
