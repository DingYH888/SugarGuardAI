"""患者管理 API 路由"""
from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse

router = APIRouter(prefix="/patients", tags=["patients"])

# 获取患者列表，使用 PatientResponse Schema 来校验、过滤和序列化返回值。
@router.get("/", response_model=List[PatientResponse])
async def list_patients(skip: int = 0, limit: int = 20):
  patients = await Patient.all().offset(skip).limit(limit)
  return patients


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: int):
  """获取单个患者详情"""
  patient = await Patient.get_or_none(id=patient_id)
  if not patient:
    raise HTTPException(status_code=404, detail="患者不存在")
  
  return patient


@router.post("/", response_model=PatientResponse)
async def create_patient(data: PatientCreate):
  """创建新患者"""
  # model_dump()：Pydantic v2的写法，将请求体转换为字典。
  patient = await Patient.create(**data.model_dump())
  return patient


@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(patient_id: int, data: PatientUpdate):
  """更新患者信息"""
  patient = await Patient.get_or_none(id=patient_id)
  if not patient:
    raise HTTPException(status_code=404, detail="患者不存在")
  
  # 提取已设置的字段进行更新
  # exclude_unset=True：排除未设置的字段。
  update_data = data.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(patient, key, value)
  
  await patient.save() # 异步保存
  return patient

@router.delete("/{patient_id}")
async def delete_patient(patient_id: int):
  """删除患者"""
  patient = await Patient.get_or_none(id=patient_id)
  if not patient:
    raise HTTPException(status_code=404, detail="患者不存在")
  
  await patient.delete() # 异步删除
  return {"message": "删除成功"}
