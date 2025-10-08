from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from typing import Optional
import uuid
import json

from models import (
    Client, Parent, ClientDiagnosis, GroupHistory,
    Subscription, RenewalHistory, ClientGroup
)
from schemas import ClientCreateSchema, ClientResponseSchema


class ClientService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def validate_uuid(self, table, id: str, entity_name: str):
        try:
            uuid.UUID(id)  # проверка на валидный UUID
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
    
    async def list_clients(self) -> list[ClientResponseSchema]:
        stmt = (
            select(Client)
            .options(
                selectinload(Client.parents),
                selectinload(Client.diagnoses),
                selectinload(Client.groups),
                selectinload(Client.group_history),
                selectinload(Client.subscriptions).selectinload(Subscription.renewal_history),
            )
        )
        result = await self.db.execute(stmt)
        db_clients = result.scalars().all()

        clients_out = []
        for client in db_clients:
            clients_out.append(
                ClientResponseSchema.model_validate(
                    {
                        "id": client.id,
                        "surname": client.surname,
                        "name": client.name,
                        "patronymic": client.patronymic,
                        "phone": client.phone,
                        "birth_date": client.birth_date,
                        "created_at": client.created_at,
                        "gender": client.gender,
                        "parents": [p.__dict__ for p in client.parents],
                        "diagnoses": [d.__dict__ for d in client.diagnoses],
                        "groups": [g.id for g in client.groups],
                        "group_history": [gh.__dict__ for gh in client.group_history],
                        "subscriptions": [
                            {
                                **s.__dict__,
                                "renewal_history": [r.__dict__ for r in s.renewal_history],
                                "days_of_week": json.loads(s.days_of_week) if s.days_of_week else [],
                            }
                            for s in client.subscriptions
                        ],
                    }
                )
            )

        return clients_out

    async def update_client(self, client_id: str, client_data: ClientCreateSchema) -> ClientResponseSchema:
        await self.validate_uuid(Client, client_id, "Client")

        # 1. Получение текущего клиента
        stmt = (
            select(Client)
            .options(
                selectinload(Client.parents),
                selectinload(Client.diagnoses),
                selectinload(Client.groups),
                selectinload(Client.group_history),
                selectinload(Client.subscriptions).selectinload(Subscription.renewal_history),
            )
            .where(Client.id == client_id)
        )
        result = await self.db.execute(stmt)
        db_client = result.scalar_one_or_none()

        if not db_client:
            raise HTTPException(404, "Client not found")

        # 2. Обновление основных данных клиента
        client_dict = client_data.model_dump(
            exclude={"parents", "diagnoses", "group_history", "subscriptions", "groups"}
        )
        for key, value in client_dict.items():
            setattr(db_client, key, value)

        # 3. Удаление старых связанных данных
        await self.db.execute(Parent.__table__.delete().where(Parent.client_id == client_id))
        await self.db.execute(ClientDiagnosis.__table__.delete().where(ClientDiagnosis.client_id == client_id))
        await self.db.execute(GroupHistory.__table__.delete().where(GroupHistory.client_id == client_id))
        await self.db.execute(ClientGroup.__table__.delete().where(ClientGroup.client_id == client_id))
        await self.db.execute(
            Subscription.__table__.delete().where(Subscription.client_id == client_id)
        )

        # 4. Добавление новых связанных данных
        # Родители
        for parent in client_data.parents:
            self.db.add(Parent(client_id=db_client.id, **parent.model_dump()))

        # Диагнозы
        for diag in client_data.diagnoses:
            self.db.add(ClientDiagnosis(client_id=db_client.id, **diag.model_dump()))

        # История групп
        for history in client_data.group_history:
            self.db.add(GroupHistory(client_id=db_client.id, **history.model_dump()))

        # Подписки
        for sub in client_data.subscriptions:
            sub_dict = sub.model_dump(exclude={"renewal_history"})
            sub_dict["days_of_week"] = json.dumps(sub_dict["days_of_week"])
            db_sub = Subscription(client_id=db_client.id, **sub_dict)
            self.db.add(db_sub)
            await self.db.flush()
            for renewal in sub.renewal_history:
                self.db.add(RenewalHistory(subscription_id=db_sub.id, **renewal.model_dump()))

        # Группы
        for group_id in client_data.groups:
            self.db.add(ClientGroup(client_id=db_client.id, group_id=group_id))

        await self.db.commit()

        # 5. Повторная загрузка со связями
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

        # 6. Формирование ответа
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
            "groups": [g.id for g in db_client_full.groups],
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

    async def delete_client(self, client_id: str):
        await self.validate_uuid(Client, client_id, "Client")

        # Удаление клиента и всех связанных данных
        await self.db.execute(Parent.__table__.delete().where(Parent.client_id == client_id))
        await self.db.execute(ClientDiagnosis.__table__.delete().where(ClientDiagnosis.client_id == client_id))
        await self.db.execute(GroupHistory.__table__.delete().where(GroupHistory.client_id == client_id))
        await self.db.execute(ClientGroup.__table__.delete().where(ClientGroup.client_id == client_id))
        await self.db.execute(
            Subscription.__table__.delete().where(Subscription.client_id == client_id)
        )
        await self.db.execute(Client.__table__.delete().where(Client.id == client_id))

        await self.db.commit()