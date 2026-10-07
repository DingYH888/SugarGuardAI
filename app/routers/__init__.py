from fastapi import APIRouter

# 从 app/routers/ 目录导入所有子路由
from app.routers import (
  patient,
  blood_sugar,
  diet_record,
  medication,
)

# 创建一个主路由，专门挂在所有的 API 
main_router = APIRouter(prefix="/api", tags=["main"])
main_router.include_router(patient.router)
main_router.include_router(blood_sugar.router)
main_router.include_router(diet_record.router)
main_router.include_router(medication.router)