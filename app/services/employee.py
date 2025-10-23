from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import Optional, List

from app.models.employee import Employee
from app.schemas import EmployeeCreate, Employee as EmployeeSchema


class EmployeeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_employee(self, employee_data: EmployeeCreate) -> EmployeeSchema:
        if not employee_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")
        if not employee_data.phone.strip():
            raise HTTPException(400, "Phone cannot be empty")

        db_employee = Employee(**employee_data.model_dump())
        self.db.add(db_employee)
        await self.db.commit()
        await self.db.refresh(db_employee)
        return EmployeeSchema.model_validate(db_employee)

    async def get_employee(self, employee_id: str) -> Optional[EmployeeSchema]:
        result = await self.db.execute(select(Employee).filter(Employee.id == employee_id))
        db_employee = result.scalar_one_or_none()
        if not db_employee:
            return None
        return EmployeeSchema.model_validate(db_employee)

    async def list_employees(self) -> List[EmployeeSchema]:
        result = await self.db.execute(select(Employee))
        employees = result.scalars().all()
        return [EmployeeSchema.model_validate(e) for e in employees]

    async def update_employee(self, employee_id: str, employee_data: EmployeeCreate) -> EmployeeSchema:
        result = await self.db.execute(select(Employee).filter(Employee.id == employee_id))
        db_employee = result.scalar_one_or_none()
        if not db_employee:
            raise HTTPException(404, "Employee not found")

        if not employee_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")
        if not employee_data.phone.strip():
            raise HTTPException(400, "Phone cannot be empty")

        db_employee.name = employee_data.name
        db_employee.position = employee_data.position
        db_employee.phone = employee_data.phone

        await self.db.commit()
        await self.db.refresh(db_employee)
        return EmployeeSchema.model_validate(db_employee)

    async def delete_employee(self, employee_id: str) -> None:
        result = await self.db.execute(select(Employee).filter(Employee.id == employee_id))
        db_employee = result.scalar_one_or_none()
        if not db_employee:
            raise HTTPException(404, "Employee not found")

        await self.db.delete(db_employee)
        await self.db.commit()
