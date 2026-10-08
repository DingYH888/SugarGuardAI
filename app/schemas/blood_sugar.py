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

#血糖统计数据响应体
class BloodSugarStatsResponse(BaseModel):
  period_days: int # 天数
  record_count: int # 记录数
  avg: float # 平均值
  min: float # 最小值
  max: float # 最大值
  std: float # 标准差
  high_count: int # 高血糖次数
  low_count: int # 低血糖次数
  normal_count: int # 正常血糖次数
  time_in_range: float # 正常血糖达标率
  trend: str # 血糖趋势
  risk_level: str # 风险等级
  error: Optional[str] = None # 错误信息

