from fastapi import APIRouter, Depends, HTTPException
from typing import List
from services import DiagnosisService
from schemas import DiagnosisCreateSchema, DiagnosisResponseSchema
from ..dependencies import get_diagnosis_service

router = APIRouter(prefix="/diagnoses", tags=["diagnoses"])

@router.post("", response_model=DiagnosisResponseSchema)
async def create_diagnosis(diagnosis_data: DiagnosisCreateSchema, service: DiagnosisService = Depends(get_diagnosis_service)):
    return await service.create_diagnosis(diagnosis_data)

@router.get("/{diagnosis_id}", response_model=DiagnosisResponseSchema)
async def get_diagnosis(diagnosis_id: str, service: DiagnosisService = Depends(get_diagnosis_service)):
    diagnosis = await service.get_diagnosis(diagnosis_id)
    if not diagnosis:
        raise HTTPException(404, "Diagnosis not found")
    return diagnosis

@router.get("", response_model=List[DiagnosisResponseSchema])
async def list_diagnoses(service: DiagnosisService = Depends(get_diagnosis_service)):
    return await service.list_diagnoses()

@router.put("/{diagnosis_id}", response_model=DiagnosisResponseSchema)
async def update_diagnosis(diagnosis_id: str, diagnosis_data: DiagnosisCreateSchema, service: DiagnosisService = Depends(get_diagnosis_service)):
    return await service.update_diagnosis(diagnosis_id, diagnosis_data)

@router.delete("/{diagnosis_id}")
async def delete_diagnosis(diagnosis_id: str, service: DiagnosisService = Depends(get_diagnosis_service)):
    await service.delete_diagnosis(diagnosis_id)
    return {"message": "Diagnosis deleted"}
