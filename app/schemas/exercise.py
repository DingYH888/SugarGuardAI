from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ExerciseBase(BaseModel):
  exercise_type: str
  duration_min: int
  intensity: str = "中等"
  calories_burned: Optional[float] = None
  performed_at: datetime
  blood_sugar_before: Optional[float] = None
  blood_sugar_after: Optional[float] = None
  note: Optional[str] = None

class ExerciseCreate(ExerciseBase):
  patient_id: int

class ExerciseUpdate(ExerciseBase):
  pass

class ExerciseResponse(ExerciseBase):
  id: int
  patient_id: int
  bs_change: Optional[float] = None # 对应模型中的 @property
  created_at: datetime

  model_config = ConfigDict(from_attributes=True)