from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime

# 患者基本信息模型
class PatientBase(BaseModel):
  name: str
  age: int
  gender: str = "未知"
  diabetes_type: str = "2型"
  diagnosis_date: Optional[date] = None # 指定类型，该数据可以缺失
  height: Optional[float] = None 
  weight: Optional[float] = None
  phone: Optional[str] = None
  emergency_contact: Optional[str] = None
  emergency_phone: Optional[str] = None
  medical_history: Optional[str] = None
  allergies: Optional[str] = None

# 患者信息的响应体
class PatientResponse(PatientBase):
  id: int
  created_at: datetime
  updated_at: datetime
  bmi: Optional[float] = None
  bmi_status: Optional[str] = None

  # Pydantic v2 的新配置写法
  # 自动调用@property方法，并赋值给响应模型的 bmi，bmi_status字段
  model_config = ConfigDict(from_attributes=True)
