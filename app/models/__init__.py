"""
模型包初始化：统一导出所有模型，便于Tortoise ORM发现并建立映射
"""
from app.models.patient import Patient
from app.models.blood_sugar import BloodSugar
from app.models.diet_record import DietRecord
from app.models.medication import Medication
from app.models.exercise import Exercise

# 供外部导入和 Tortoise 配置引用
__all__ = [
  "Patient",
  "BloodSugar",
  "DietRecord",
  "Medication",
  "Exercise",
]
