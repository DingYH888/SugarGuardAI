""" 患者管理 API 路由 """
from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.patient import Patient
from app.schemas.patient import PatientResponse

router = APIRouter(prefix="/patients",tags=["patients"])

# 获取患者列表，使用 PatientResponse Schema 来校验，过滤和序列化返回值
@router.get("/",response_model=List[PatientResponse])
async def list_patients(skip:int=0 , limit:int=20):
  patients = await Patient.all().offset(skip).limit(limit)
  return patients
