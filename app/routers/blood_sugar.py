"""血糖记录 API 路由。"""
from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Query, HTTPException
from tortoise.expressions import Q
from app.models.patient import Patient
from app.models.blood_sugar import BloodSugar
from app.schemas.blood_sugar import BloodSugarCreate, BloodSugarUpdate, BloodSugarResponse

router = APIRouter(prefix="/blood-sugar", tags=["blood-sugar"])

# 创建血糖记录
@router.post("/", response_model=BloodSugarResponse)
async def create_record(data: BloodSugarCreate):
  await Patient.get_or_none(id=data.patient_id) # 检查患者是否存在
  record = await BloodSugar.create(**data.model_dump()) # 创建血糖记录
  return BloodSugarResponse(
    id=record.id,
    patient_id=record.patient_id,
    value=record.value,
    measure_type=record.measure_type,
    measured_at=record.measured_at,
    note=record.note,
    status=record.status,
    created_at=record.created_at,
   )


# 获取患者血糖记录
# days 默认 7 天，范围 1~90
@router.get("/patient/{patient_id}", response_model=List[BloodSugarResponse])
async def get_records(patient_id: int, days: int = Query(7, ge=1, le=90)):
  await Patient.get_or_none(id=patient_id) # 检查患者是否存在
  # 获取指定天数内的血糖记录，从当前时间往前推
  since = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days) 
  # 查询指定患者在指定天数内的血糖记录，并按测量时间降序排序
  records = await BloodSugar.filter(
    Q(patient_id=patient_id) & Q(measured_at__gte=since)
   ).order_by("-measured_at").all()
  return [
    BloodSugarResponse(
      id=r.id,
      patient_id=r.patient_id,
      value=r.value,
      measure_type=r.measure_type,
      measured_at=r.measured_at,
      note=r.note,
      status=r.status,
      created_at=r.created_at,
     )
    for r in records
   ]

# 更新血糖记录
@router.put("/{record_id}", response_model=BloodSugarResponse)
async def update_record(record_id: int, data: BloodSugarUpdate):
  record = await BloodSugar.get_or_none(id=record_id) # 检查血糖记录是否存在
  if not record:
    raise HTTPException(status_code=404, detail="血糖记录不存在")

  update_data = data.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(record, key, value)

  # 写回数据库并重新加载数据
  await record.save()
  await record.refresh_from_db()

  return BloodSugarResponse(
    id=record.id,
    patient_id=record.patient_id,
    value=record.value,
    measure_type=record.measure_type,
    measured_at=record.measured_at,
    note=record.note,
    status=record.status,
    created_at=record.created_at,
   )

# 删除血糖记录
@router.delete("/{record_id}")
async def delete_record(record_id: int):
  record = await BloodSugar.get_or_none(id=record_id)
  if not record:
    raise HTTPException(status_code=404, detail="血糖记录不存在")
  await record.delete()
  return {"message": "删除成功"}
