import uuid
from datetime import date
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    creation_date = Column(Date, nullable=False, default=date.today)

    subscriptions = relationship("Subscription", backref="contract")
