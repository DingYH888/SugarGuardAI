"""用药管理 API 路由"""
from typing import List

from fastapi import APIRouter, HTTPException
from tortoise.expressions import Q

from app.models.patient import Patient
from app.models.medication import Medication
from app.schemas.medication import MedicationCreate, MedicationResponse, MedicationUpdate

router = APIRouter(prefix="/medication", tags=["medication"])

# 获取患者用药记录
@router.get("/patient/{patient_id}", response_model=List[MedicationResponse])
async def get_medications(patient_id: int, active_only: bool = True):
  await Patient.get_or_none(id=patient_id)
  query = Medication.filter(patient_id=patient_id)
  if active_only:
    query = query.filter(is_active=True)
  records = await query.order_by("-start_date").all()
  return [
    MedicationResponse(
      id=r.id,
      patient_id=r.patient_id,
      drug_name=r.drug_name,
      drug_type=r.drug_type,
      dosage=r.dosage,
      frequency=r.frequency,
      timing=r.timing,
      start_date=r.start_date,
      end_date=r.end_date,
      is_active=r.is_active,
      side_effects=r.side_effects,
      note=r.note,
      created_at=r.created_at,
     )
    for r in records
   ]

# 新增用药记录
@router.post("/", response_model=MedicationResponse)
async def create_medication(data: MedicationCreate):
  await Patient.get_or_none(id=data.patient_id)
  record = await Medication.create(**data.model_dump())
  return MedicationResponse(
    id=record.id,
    patient_id=record.patient_id,
    drug_name=record.drug_name,
    drug_type=record.drug_type,
    dosage=record.dosage,
    frequency=record.frequency,
    timing=record.timing,
    start_date=record.start_date,
    end_date=record.end_date,
    is_active=record.is_active,
    side_effects=record.side_effects,
    note=record.note,
    created_at=record.created_at,
   )

# 更新用药记录
@router.put("/{medication_id}", response_model=MedicationResponse)
async def update_medication(medication_id: int, data: MedicationUpdate):
  record = await Medication.get_or_none(id=medication_id)
  if not record:
    raise HTTPException(status_code=404, detail="用药记录不存在")

  update_data = data.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(record, key, value)

  await record.save()
  await record.refresh_from_db()

  return MedicationResponse(
    id=record.id,
    patient_id=record.patient_id,
    drug_name=record.drug_name,
    drug_type=record.drug_type,
    dosage=record.dosage,
    frequency=record.frequency,
    timing=record.timing,
    start_date=record.start_date,
    end_date=record.end_date,
    is_active=record.is_active,
    side_effects=record.side_effects,
    note=record.note,
    created_at=record.created_at,
   )

# 删除用药记录
@router.delete("/{medication_id}")
async def delete_medication(medication_id: int):
  record = await Medication.get_or_none(id=medication_id)
  if not record:
    raise HTTPException(status_code=404, detail="用药记录不存在")
  await record.delete()
  return {"message": "删除成功"}
