from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime

# 健康报告响应体
class HealthReportResponse(BaseModel):
  """健康报告响应模型"""
  id: int  # 报告唯一标识
  patient: int  # 患者标识
  report_type: str  # 报告类型
  period_start: date  # 统计周期开始日期
  period_end: date  # 统计周期结束日期
  avg_blood_sugar: Optional[float] = None  # 平均血糖值，可为空
  blood_sugar_std: Optional[float] = None  # 血糖标准差，可为空
  time_in_range: Optional[float] = None  # 血糖在目标范围内的时间占比，可为空
  summary: str  # 报告摘要
  recommendations: Optional[str] = None  # 建议内容，可为空
  risk_level: Optional[str] = None  # 风险等级，可为空
  generated_at: datetime  # 报告生成时间
