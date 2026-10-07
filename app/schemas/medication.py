from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime

class MedicationBase(BaseModel):
  drug_name: str
  drug_type: Optional[str] = None
  dosage: str
  frequency: Optional[str] = None
  timing: Optional[str] = None
  start_date: date
  end_date: Optional[date] = None
  is_active: bool = True
  side_effects: Optional[str] = None
  note: Optional[str] = None

class MedicationCreate(MedicationBase):
  patient_id: int

class MedicationUpdate(BaseModel):
  drug_name: Optional[str] = None
  dosage: Optional[str] = None
  frequency: Optional[str] = None
  timing: Optional[str] = None
  end_date: Optional[date] = None
  is_active: Optional[bool] = None
  note: Optional[str] = None

class MedicationResponse(MedicationBase):
  id: int
  patient_id: int
  created_at: datetime

  model_config = ConfigDict(from_attributes=True)
