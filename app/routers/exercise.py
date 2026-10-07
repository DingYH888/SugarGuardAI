"""运动记录 API 路由。"""
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException
from tortoise.expressions import Q
from app.models.patient import Patient
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseResponse

router = APIRouter(prefix="/exercise", tags=["exercise"])


# 创建运动记录
@router.post("/", response_model=ExerciseResponse)
async def create_record(data: ExerciseCreate):
  await Patient.get_or_none(id=data.patient_id)
  record = await Exercise.create(**data.model_dump())

  return ExerciseResponse(
    id=record.id,
    patient_id=record.patient_id,
    exercise_type=record.exercise_type,
    duration_min=record.duration_min,
    intensity=record.intensity,
    calories_burned=record.calories_burned,
    performed_at=record.performed_at,
    blood_sugar_before=record.blood_sugar_before,
    blood_sugar_after=record.blood_sugar_after,
    note=record.note,
    bs_change=record.bs_change,
    created_at=record.created_at
   )


# 获取患者运动记录
@router.get("/patient/{patient_id}", response_model=List[ExerciseResponse])
async def get_records(patient_id: int,limit:int = 30):
  await Patient.get_or_none(id=patient_id)
  records = await Exercise.filter(patient_id=patient_id).order_by("-performed_at").limit(limit).all()

  return [
    ExerciseResponse(
      id=record.id,
      patient_id=record.patient_id,
      exercise_type=record.exercise_type,
      duration_min=record.duration_min,
      intensity=record.intensity,
      calories_burned=record.calories_burned,
      performed_at=record.performed_at,
      blood_sugar_before=record.blood_sugar_before,
      blood_sugar_after=record.blood_sugar_after,
      note=record.note,
      bs_change=record.bs_change,
      created_at=record.created_at
     )
    for record in records
   ]


# 更新运动记录
@router.put("/{record_id}", response_model=ExerciseResponse)
async def update_record(record_id: int, data: ExerciseUpdate):
  record = await Exercise.get_or_none(id=record_id)
  if not record:
    raise HTTPException(status_code=404, detail="运动记录不存在")

  await record.update_from_dict(data.model_dump())
  await record.save()

  return ExerciseResponse(
    id=record.id,
    patient_id=record.patient_id,
    exercise_type=record.exercise_type,
    duration_min=record.duration_min,
    intensity=record.intensity,
    calories_burned=record.calories_burned,
    performed_at=record.performed_at,
    blood_sugar_before=record.blood_sugar_before,
    blood_sugar_after=record.blood_sugar_after,
    note=record.note,
    bs_change=record.bs_change,
    created_at=record.created_at
   )


# 删除运动记录
@router.delete("/{record_id}")
async def delete_record(record_id: int):
  record = await Exercise.get_or_none(id=record_id)
  if not record:
    raise HTTPException(status_code=404, detail="运动记录不存在")
  await record.delete()
  return {"message": "删除成功"}
