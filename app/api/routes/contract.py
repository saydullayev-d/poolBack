from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.auth import get_current_user
from app.models import User
from app.models.database import get_db
from app.services.contract import ContractService
from app.schemas import Contract, ContractCreate

router = APIRouter(prefix="/contracts", tags=["Contracts"])


@router.post("/", response_model=Contract)
async def create_contract(data: ContractCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ContractService(db).create_contract(data)


@router.get("/{contract_id}", response_model=Contract)
async def get_contract(contract_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    contract = await ContractService(db).get_contract(contract_id)
    if not contract:
        raise HTTPException(404, "Contract not found")
    return contract


@router.get("/", response_model=List[Contract])
async def list_contracts(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ContractService(db).list_contracts()


@router.put("/{contract_id}", response_model=Contract)
async def update_contract(contract_id: str, data: ContractCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ContractService(db).update_contract(contract_id, data)


@router.delete("/{contract_id}")
async def delete_contract(contract_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    await ContractService(db).delete_contract(contract_id)
    return {"message": "Contract deleted"}
