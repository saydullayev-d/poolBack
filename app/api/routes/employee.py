from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.auth import get_current_user
from app.models import User
from app.models.database import get_db
from app.services.employee import EmployeeService
from app.schemas import Employee, EmployeeCreate

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/", response_model=Employee)
async def create_employee(data: EmployeeCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await EmployeeService(db).create_employee(data)


@router.get("/{employee_id}", response_model=Employee)
async def get_employee(employee_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    employee = await EmployeeService(db).get_employee(employee_id)
    if not employee:
        raise HTTPException(404, "Employee not found")
    return employee


@router.get("/", response_model=List[Employee])
async def list_employees(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await EmployeeService(db).list_employees()


@router.put("/{employee_id}", response_model=Employee)
async def update_employee(employee_id: str, data: EmployeeCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await EmployeeService(db).update_employee(employee_id, data)


@router.delete("/{employee_id}")
async def delete_employee(employee_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    await EmployeeService(db).delete_employee(employee_id)
    return {"message": "Employee deleted"}
