from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import Optional, List

from app.models.contract import Contract
from app.schemas import ContractCreate, Contract as ContractSchema


class ContractService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_contract(self, contract_data: ContractCreate) -> ContractSchema:
        db_contract = Contract(**contract_data.model_dump(exclude={"subscriptions"}))

        # если у контракта есть подписки — пока просто игнорим (логика привязки в сервисе подписок)
        self.db.add(db_contract)
        await self.db.commit()
        await self.db.refresh(db_contract)
        return ContractSchema.model_validate(db_contract)

    async def get_contract(self, contract_id: str) -> Optional[ContractSchema]:
        result = await self.db.execute(select(Contract).filter(Contract.id == contract_id))
        db_contract = result.scalar_one_or_none()
        if not db_contract:
            return None
        return ContractSchema.model_validate(db_contract)

    async def list_contracts(self) -> List[ContractSchema]:
        result = await self.db.execute(select(Contract))
        contracts = result.scalars().all()
        return [ContractSchema.model_validate(c) for c in contracts]

    async def update_contract(self, contract_id: str, contract_data: ContractCreate) -> ContractSchema:
        result = await self.db.execute(select(Contract).filter(Contract.id == contract_id))
        db_contract = result.scalar_one_or_none()
        if not db_contract:
            raise HTTPException(404, "Contract not found")

        db_contract.creation_date = contract_data.creation_date
        # subscriptions пока не обновляем, нужна отдельная логика

        await self.db.commit()
        await self.db.refresh(db_contract)
        return ContractSchema.model_validate(db_contract)

    async def delete_contract(self, contract_id: str) -> None:
        result = await self.db.execute(select(Contract).filter(Contract.id == contract_id))
        db_contract = result.scalar_one_or_none()
        if not db_contract:
            raise HTTPException(404, "Contract not found")

        await self.db.delete(db_contract)
        await self.db.commit()
