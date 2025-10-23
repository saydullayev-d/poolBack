import uuid
from sqlalchemy import Column, String, Date, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    template_id = Column(String, ForeignKey("subscription_templates.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    classes_per_week = Column(Integer, nullable=False)
    days_of_week = Column(String, nullable=True)  # Store as JSON string
    class_time = Column(String, nullable=False)
    group_id = Column(String, ForeignKey("groups.id"), nullable=True)
    remaining_classes = Column(Integer, nullable=False)
    is_paid = Column(Boolean, default=True)
    subscription_number = Column(String, unique=True, nullable=False)
    contract_id = Column(String, ForeignKey("contracts.id"), nullable=True)

    renewal_history = relationship("RenewalHistory", backref="subscription")
