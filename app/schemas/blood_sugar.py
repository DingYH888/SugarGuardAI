from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class BloodSugarBase(BaseModel):
  value: float
  measure_type: str
  measured_at: datetime
  note: Optional[str] = None

class BloodSugarCreate(BloodSugarBase):
  patient_id: int

class BloodSugarUpdate(BaseModel):
  value: Optional[float] = None
  measure_type: Optional[str] = None
  measured_at: Optional[datetime] = None
  note: Optional[str] = None

class BloodSugarResponse(BloodSugarBase):
  id: int
  patient_id: int
  status: Optional[str] = None
  created_at: datetime

  model_config = ConfigDict(from_attributes=True)
