from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from models.client import Client, Parent, ClientDiagnosis, GroupHistory, Subscription, RenewalHistory, ClientGroup, Relation, Diagnosis, Group, SubscriptionTemplate
from api.schemas import ClientCreateSchema, ClientResponseSchema, RelationCreateSchema, RelationResponseSchema, DiagnosisCreateSchema, DiagnosisResponseSchema, GroupCreateSchema, GroupResponseSchema, SubscriptionTemplateCreateSchema, SubscriptionTemplateResponseSchema
from typing import Optional, List
from fastapi import HTTPException
import json
import uuid

class RelationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_relation(self, relation_data: RelationCreateSchema) -> RelationResponseSchema:
        if not relation_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")
        db_relation = Relation(**relation_data.model_dump())
        self.db.add(db_relation)
        await self.db.commit()
        await self.db.refresh(db_relation)
        return RelationResponseSchema.model_validate(db_relation)

    async def get_relation(self, relation_id: str) -> Optional[RelationResponseSchema]:
        result = await self.db.execute(select(Relation).filter(Relation.id == relation_id))
        db_relation = result.scalar_one_or_none()
        if not db_relation:
            return None
        return RelationResponseSchema.model_validate(db_relation)

    async def list_relations(self) -> List[RelationResponseSchema]:
        result = await self.db.execute(select(Relation))
        relations = result.scalars().all()
        return [RelationResponseSchema.model_validate(r) for r in relations]

    async def update_relation(self, relation_id: str, relation_data: RelationCreateSchema) -> RelationResponseSchema:
        result = await self.db.execute(select(Relation).filter(Relation.id == relation_id))
        db_relation = result.scalar_one_or_none()
        if not db_relation:
            raise HTTPException(404, "Relation not found")
        if not relation_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")
        db_relation.name = relation_data.name
        await self.db.commit()
        await self.db.refresh(db_relation)
        return RelationResponseSchema.model_validate(db_relation)

    async def delete_relation(self, relation_id: str) -> None:
        result = await self.db.execute(select(Relation).filter(Relation.id == relation_id))
        db_relation = result.scalar_one_or_none()
        if not db_relation:
            raise HTTPException(404, "Relation not found")
        await self.db.delete(db_relation)
        await self.db.commit()

class DiagnosisService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_diagnosis(self, diagnosis_data: DiagnosisCreateSchema) -> DiagnosisResponseSchema:
        if not diagnosis_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")
        db_diagnosis = Diagnosis(**diagnosis_data.model_dump())
        self.db.add(db_diagnosis)
        await self.db.commit()
        await self.db.refresh(db_diagnosis)
        return DiagnosisResponseSchema.model_validate(db_diagnosis)

    async def get_diagnosis(self, diagnosis_id: str) -> Optional[DiagnosisResponseSchema]:
        result = await self.db.execute(select(Diagnosis).filter(Diagnosis.id == diagnosis_id))
        db_diagnosis = result.scalar_one_or_none()
        if not db_diagnosis:
            return None
        return DiagnosisResponseSchema.model_validate(db_diagnosis)

    async def list_diagnoses(self) -> List[DiagnosisResponseSchema]:
        result = await self.db.execute(select(Diagnosis))
        diagnoses = result.scalars().all()
        return [DiagnosisResponseSchema.model_validate(d) for d in diagnoses]

    async def update_diagnosis(self, diagnosis_id: str, diagnosis_data: DiagnosisCreateSchema) -> DiagnosisResponseSchema:
        result = await self.db.execute(select(Diagnosis).filter(Diagnosis.id == diagnosis_id))
        db_diagnosis = result.scalar_one_or_none()
        if not db_diagnosis:
            raise HTTPException(404, "Diagnosis not found")
        if not diagnosis_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")
        db_diagnosis.name = diagnosis_data.name
        await self.db.commit()
        await self.db.refresh(db_diagnosis)
        return DiagnosisResponseSchema.model_validate(db_diagnosis)

    async def delete_diagnosis(self, diagnosis_id: str) -> None:
        result = await self.db.execute(select(Diagnosis).filter(Diagnosis.id == diagnosis_id))
        db_diagnosis = result.scalar_one_or_none()
        if not db_diagnosis:
            raise HTTPException(404, "Diagnosis not found")
        await self.db.delete(db_diagnosis)
        await self.db.commit()

class GroupService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_group(self, group_data: GroupCreateSchema) -> GroupResponseSchema:
        if not group_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")
        db_group = Group(**group_data.model_dump())
        self.db.add(db_group)
        await self.db.commit()
        await self.db.refresh(db_group)
        return GroupResponseSchema.model_validate(db_group)

    async def get_group(self, group_id: str) -> Optional[GroupResponseSchema]:
        result = await self.db.execute(select(Group).filter(Group.id == group_id))
        db_group = result.scalar_one_or_none()
        if not db_group:
            return None
        return GroupResponseSchema.model_validate(db_group)

    async def list_groups(self) -> List[GroupResponseSchema]:
        result = await self.db.execute(select(Group))
        groups = result.scalars().all()
        return [GroupResponseSchema.model_validate(g) for g in groups]

    async def update_group(self, group_id: str, group_data: GroupCreateSchema) -> GroupResponseSchema:
        result = await self.db.execute(select(Group).filter(Group.id == group_id))
        db_group = result.scalar_one_or_none()
        if not db_group:
            raise HTTPException(404, "Group not found")
        if not group_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")
        db_group.name = group_data.name
        await self.db.commit()
        await self.db.refresh(db_group)
        return GroupResponseSchema.model_validate(db_group)

    async def delete_group(self, group_id: str) -> None:
        result = await self.db.execute(select(Group).filter(Group.id == group_id))
        db_group = result.scalar_one_or_none()
        if not db_group:
            raise HTTPException(404, "Group not found")
        await self.db.delete(db_group)
        await self.db.commit()

class SubscriptionTemplateService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_subscription_template(self, template_data: SubscriptionTemplateCreateSchema) -> SubscriptionTemplateResponseSchema:
        if not template_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")
        db_template = SubscriptionTemplate(**template_data.model_dump())
        self.db.add(db_template)
        await self.db.commit()
        await self.db.refresh(db_template)
        return SubscriptionTemplateResponseSchema.model_validate(db_template)

    async def get_subscription_template(self, template_id: str) -> Optional[SubscriptionTemplateResponseSchema]:
        result = await self.db.execute(select(SubscriptionTemplate).filter(SubscriptionTemplate.id == template_id))
        db_template = result.scalar_one_or_none()
        if not db_template:
            return None
        return SubscriptionTemplateResponseSchema.model_validate(db_template)

    async def list_subscription_templates(self) -> List[SubscriptionTemplateResponseSchema]:
        result = await self.db.execute(select(SubscriptionTemplate))
        templates = result.scalars().all()
        return [SubscriptionTemplateResponseSchema.model_validate(t) for t in templates]

    async def update_subscription_template(self, template_id: str, template_data: SubscriptionTemplateCreateSchema) -> SubscriptionTemplateResponseSchema:
        result = await self.db.execute(select(SubscriptionTemplate).filter(SubscriptionTemplate.id == template_id))
        db_template = result.scalar_one_or_none()
        if not db_template:
            raise HTTPException(404, "SubscriptionTemplate not found")
        if not template_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")
        db_template.name = template_data.name
        await self.db.commit()
        await self.db.refresh(db_template)
        return SubscriptionTemplateResponseSchema.model_validate(db_template)

    async def delete_subscription_template(self, template_id: str) -> None:
        result = await self.db.execute(select(SubscriptionTemplate).filter(SubscriptionTemplate.id == template_id))
        db_template = result.scalar_one_or_none()
        if not db_template:
            raise HTTPException(404, "SubscriptionTemplate not found")
        await self.db.delete(db_template)
        await self.db.commit()

class ClientService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def validate_uuid(self, table, id: str, entity_name: str):
        try:
            uuid.UUID(id)  # Check if valid UUID
        except ValueError:
            raise HTTPException(400, f"Invalid UUID for {entity_name}")
        result = await self.db.execute(select(table).filter(table.id == id))
        if not result.scalar_one_or_none():
            raise HTTPException(404, f"{entity_name} not found")


    async def create_client(self, client_data: ClientCreateSchema) -> ClientResponseSchema:
    # 1. Основные данные клиента
        client_dict = client_data.model_dump(
            exclude={"parents", "diagnoses", "group_history", "subscriptions", "groups"}
        )
        db_client = Client(**client_dict)
        self.db.add(db_client)
        await self.db.flush()  # чтобы id появился

        # 2. Родители
        for parent in client_data.parents:
            self.db.add(Parent(client_id=db_client.id, **parent.model_dump()))

        # 3. Диагнозы
        for diag in client_data.diagnoses:
            self.db.add(ClientDiagnosis(client_id=db_client.id, **diag.model_dump()))

        # 4. История групп
        for history in client_data.group_history:
            self.db.add(GroupHistory(client_id=db_client.id, **history.model_dump()))

        # 5. Подписки
        for sub in client_data.subscriptions:
            sub_dict = sub.model_dump(exclude={"renewal_history"})
            sub_dict["days_of_week"] = json.dumps(sub_dict["days_of_week"])
            db_sub = Subscription(client_id=db_client.id, **sub_dict)
            self.db.add(db_sub)
            await self.db.flush()
            for renewal in sub.renewal_history:
                self.db.add(RenewalHistory(subscription_id=db_sub.id, **renewal.model_dump()))

        # 6. Группы
        for group_id in client_data.groups:
            self.db.add(ClientGroup(client_id=db_client.id, group_id=group_id))

        await self.db.commit()

        # 7. Повторная загрузка со связями
        stmt = (
            select(Client)
            .options(
                selectinload(Client.parents),
                selectinload(Client.diagnoses),
                selectinload(Client.groups),
                selectinload(Client.group_history),
                selectinload(Client.subscriptions).selectinload(Subscription.renewal_history),
            )
            .where(Client.id == db_client.id)
        )
        result = await self.db.execute(stmt)
        db_client_full = result.scalar_one()

        # 8. Приведение к dict перед Pydantic
        client_out = {
            "id": db_client_full.id,
            "surname": db_client_full.surname,
            "name": db_client_full.name,
            "patronymic": db_client_full.patronymic,
            "phone": db_client_full.phone,
            "birth_date": db_client_full.birth_date,
            "created_at": db_client_full.created_at,
            "gender": db_client_full.gender,
            "parents": [p.__dict__ for p in db_client_full.parents],
            "diagnoses": [d.__dict__ for d in db_client_full.diagnoses],
            "groups": [g.id for g in db_client_full.groups],  # берём только id
            "group_history": [gh.__dict__ for gh in db_client_full.group_history],
            "subscriptions": [
                {
                    **s.__dict__,
                    "renewal_history": [r.__dict__ for r in s.renewal_history],
                    "days_of_week": json.loads(s.days_of_week) if s.days_of_week else [],
                }
                for s in db_client_full.subscriptions
            ],
        }

        return ClientResponseSchema.model_validate(client_out)

    async def get_client(self, client_id: str) -> Optional[ClientResponseSchema]:
        result = await self.db.execute(select(Client).filter(Client.id == client_id))
        db_client = result.scalar_one_or_none()
        if not db_client:
            return None
        for sub in db_client.subscriptions:
            if sub.days_of_week:
                sub.days_of_week = json.loads(sub.days_of_week)
        return ClientResponseSchema.model_validate(db_client)