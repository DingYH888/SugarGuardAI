"""饮食管理 API 路由。"""
from typing import List, Optional

from fastapi import APIRouter, HTTPException,Query
from tortoise.expressions import Q

from app.core.diet_advisor import diet_advisor
from app.models.patient import Patient
from app.models.diet_record import DietRecord
from app.schemas.diet_record import DietRecordCreate, DietRecordUpdate, DietRecordResponse

router = APIRouter(prefix="/diet", tags=["diet"])

# 创建饮食记录
@router.post("/", response_model=DietRecordResponse)
async def create_record(data: DietRecordCreate):
  await Patient.get_or_none(id=data.patient_id)
  record = await DietRecord.create(**data.model_dump())
  return DietRecordResponse(
    id=record.id,
    patient_id=record.patient_id,
    food_name=record.food_name,
    calories=record.calories,
    carbs=record.carbs,
    protein=record.protein,
    fat=record.fat,
    gi_value=record.gi_value,
    portion=record.portion,
    meal_type=record.meal_type,
    eaten_at=record.eaten_at,
    note=record.note,
    gi_level=record.gi_level,
    created_at=record.created_at,
   )

# 获取患者饮食记录
@router.get("/patient/{patient_id}/records", response_model=List[DietRecordResponse])
async def get_records(patient_id: int, limit: int = 50):
  await Patient.get_or_none(id=patient_id)
  records = await DietRecord.filter(patient_id=patient_id).order_by("-eaten_at").limit(limit).all()
  return [
    DietRecordResponse(
      id=r.id,
      patient_id=r.patient_id,
      food_name=r.food_name,
      calories=r.calories,
      carbs=r.carbs,
      protein=r.protein,
      fat=r.fat,
      gi_value=r.gi_value,
      portion=r.portion,
      meal_type=r.meal_type,
      eaten_at=r.eaten_at,
      note=r.note,
      gi_level=r.gi_level,
      created_at=r.created_at,
     )
    for r in records
   ]

# 更新饮食记录
@router.put("/{record_id}", response_model=DietRecordResponse)
async def update_record(record_id: int, data: DietRecordUpdate):
  record = await DietRecord.get_or_none(id=record_id)
  if not record:
    raise HTTPException(status_code=404, detail="饮食记录不存在")

  update_data = data.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(record, key, value)

  await record.save()
  await record.refresh_from_db()

  return DietRecordResponse(
    id=record.id,
    patient_id=record.patient_id,
    food_name=record.food_name,
    calories=record.calories,
    carbs=record.carbs,
    protein=record.protein,
    fat=record.fat,
    gi_value=record.gi_value,
    portion=record.portion,
    meal_type=record.meal_type,
    eaten_at=record.eaten_at,
    note=record.note,
    gi_level=record.gi_level,
    created_at=record.created_at,
   )

# 删除饮食记录
@router.delete("/{record_id}")
async def delete_record(record_id: int):
  record = await DietRecord.get_or_none(id=record_id)
  if not record:
    raise HTTPException(status_code=404, detail="饮食记录不存在")
  await record.delete()
  return {"message": "删除成功"}

# 每日营养统计
@router.get("/patient/{patient_id}/daily")
async def get_daily_nutrition(patient_id: int, date: Optional[str] = Query(default=None)):
  patient = await Patient.get_or_none(id=patient_id)
  if not patient:
    raise HTTPException(status_code=404, detail="患者不存在")
  return await diet_advisor.get_daily_nutrition(patient_id, date)
