from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class DietRecordBase(BaseModel):
  food_name: str
  calories: Optional[float] = None
  carbs: Optional[float] = None
  protein: Optional[float] = None
  fat: Optional[float] = None
  gi_value: Optional[float] = None
  portion: Optional[float] = 1.0
  meal_type: Optional[str] = None
  eaten_at: datetime
  note: Optional[str] = None

class DietRecordCreate(DietRecordBase):
  patient_id: int

class DietRecordUpdate(BaseModel):
  food_name: Optional[str] = None
  calories: Optional[float] = None
  carbs: Optional[float] = None
  protein: Optional[float] = None
  fat: Optional[float] = None
  gi_value: Optional[float] = None
  portion: Optional[float] = None
  meal_type: Optional[str] = None
  eaten_at: Optional[datetime] = None
  note: Optional[str] = None

class DietRecordResponse(DietRecordBase):
  id: int
  patient_id: int
  gi_level: Optional[str] = None 
  created_at: datetime

  model_config = ConfigDict(from_attributes=True)

