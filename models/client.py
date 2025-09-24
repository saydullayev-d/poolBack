import uuid
import json
from datetime import datetime, date
from sqlalchemy import Column, String, Date, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import Base

class Relation(Base):
    __tablename__ = "relations"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)  # e.g., 'Mother'

class Diagnosis(Base):
    __tablename__ = "diagnoses"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)  # e.g., 'Scoliosis'

class Group(Base):
    __tablename__ = "groups"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)

class SubscriptionTemplate(Base):
    __tablename__ = "subscription_templates"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)

class Parent(Base):
    __tablename__ = "parents"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    relation_id = Column(String, ForeignKey("relations.id"), nullable=False)
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)

class ClientDiagnosis(Base):
    __tablename__ = "client_diagnoses"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    diagnosis_id = Column(String, ForeignKey("diagnoses.id"), nullable=False)
    notes = Column(String, nullable=True)

class GroupHistory(Base):
    __tablename__ = "group_histories"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    date = Column(Date, nullable=False)
    action = Column(String, nullable=False)  # 'added' or 'removed', validated in service
    group_id = Column(String, ForeignKey("groups.id"), nullable=False)

class RenewalHistory(Base):
    __tablename__ = "renewal_histories"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    subscription_id = Column(String, ForeignKey("subscriptions.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    from_template_id = Column(String, ForeignKey("subscription_templates.id"), nullable=True)
    to_template_id = Column(String, ForeignKey("subscription_templates.id"), nullable=False)

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
    renewal_history = relationship("RenewalHistory", backref="subscription")

class ClientGroup(Base):
    __tablename__ = "client_groups"
    client_id = Column(String, ForeignKey("clients.id"), primary_key=True)
    group_id = Column(String, ForeignKey("groups.id"), primary_key=True)

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
    photo = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    parents = relationship("Parent", backref="client")
    diagnoses = relationship("ClientDiagnosis", backref="client")
    group_history = relationship("GroupHistory", backref="client")
    subscriptions = relationship("Subscription", backref="client")
    groups = relationship("Group", secondary="client_groups", backref="clients")