import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, Boolean, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class Client(Base):
    __tablename__ = "clients"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    surname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    phone = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(String, nullable=False)  # 'male' or 'female', validated in service
    features = Column(String, nullable=True)
    blacklisted = Column(Boolean, default=False)
    photo_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    parents = relationship("Parent", backref="client", lazy="selectin")
    diagnoses = relationship("ClientDiagnosis", backref="client", lazy="selectin")
    group_history = relationship("GroupHistory", backref="client", lazy="selectin")
    subscriptions = relationship("Subscription", backref="client", lazy="selectin")
    groups = relationship("Group", secondary="client_groups", backref="clients", lazy="selectin")
