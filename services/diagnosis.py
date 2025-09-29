from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import Optional, List

from models import Diagnosis
from schemas import DiagnosisCreateSchema, DiagnosisResponseSchema


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
