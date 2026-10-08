"""健康数据分析引擎：负责血糖数据的数学统计、趋势识别及风险等级评估。"""
import statistics
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Any, Dict, List
from app.models import BloodSugar

# 加载环境变量
load_dotenv()
# 低血糖阈值
BG_LOW_THRESHOLD = float(os.getenv("BG_LOW_THRESHOLD", "3.9"))
# 高血糖阈值
BG_HIGH_THRESHOLD = float(os.getenv("BG_HIGH_THRESHOLD", "10.0"))

class HealthAnalyzer:
  async def analyze_blood_sugar(self, patient_id: int, days: int = 7) -> Dict[str, Any]:
    """
     分析患者近N天的血糖数据
     patient_id：患者ID
     days
     return：血糖分析结果字典
     """

    # 计算统计起始日期
    since = datetime.utcnow() - timedelta(days=days)
    # 获取患者指定天数内所有血糖记录
    records = await BloodSugar.filter(
      patient_id=patient_id,
      measured_at__gte=since
     ).order_by('measured_at')
    # 如果未查到数据，返回错误信息
    if not records:
      return {
        'error': '暂无血糖数据',
        "preiod_days": days,
        "record_count": 0,
        "avg": 0.0,
        "min": 0.0,
        "max": 0.0,
        "std": 0.0,
        "high_count": 0,
        "low_count": 0,
        "time_in_range": 0.0,
        "trend":"数据不足",
        "risk_level": "低风险"
       }
    # 提取数值列表用于数学计算
    values:List[float] = [record.value for record in records]
    # 高血糖次数
    high_count = sum(1 for value in values if value > BG_HIGH_THRESHOLD)
    # 低血糖次数
    low_count = sum(1 for value in values if value < BG_LOW_THRESHOLD)
    # 达标次数
    normal_count = len(values) - high_count - low_count

    return {
      "period_days": days, # 统计天数
      "record_count": len(values), # 记录数
      "avg": round(statistics.mean(values), 1), # 平均血糖
      "min": round(min(values), 1), # 最小血糖
      "max": round(max(values), 1), # 最大血糖
      "std": round(statistics.stdev(values), 2) if len(values) > 1 else 0.0, # 标准差
      "high_count": high_count, # 高血糖次数
      "low_count": low_count, # 低血糖次数
      "normal_count": normal_count, # 达标次数
      "time_in_range": round(normal_count / len(values) * 100, 1), # 达标率
      "trend":self._calculate_trend(values), # 趋势
      "risk_level": self._assess_risk(values,high_count,low_count) # 风险等级
     }
  
  def _calculate_trend(self, values:List[float]) -> str:
    """ 分析血糖趋势 """
    if len(values) < 3:
      return "数据不足"
    # 取最近3次记录
    recent = values[-3:]
    # 如果数据总数大于3条，取除了最后3条以外的前面所有数据作为“早期基准”
    # 否则取第一条数据作为早期基准
    earlier = values[:-3] if len(values) > 3 else values[:1]
    # 计算最近3次记录的平均值与早期基准的平均值的差
    diff = statistics.mean(recent) - statistics.mean(earlier)

    if diff > 0.5:
      return "上升"
    if diff < -0.5:
      return "下降"
    return "稳定"
  
  def _assess_risk(self, values:List[float],high_count:int,low_count:int) -> str:
    """ 评估血糖风险等级 """
    # 计算平均血糖
    avg = statistics.mean(values)
    # 如果低血糖次数大于等于2次或最大值大于16.7，返回高风险
    if low_count >= 2 or max(values) > 16.7:
      return "高风险"
    # 如果高血糖次数大于等于3次或平均血糖大于8.5，返回中风险
    if high_count >= 3 or avg > 8.5:
      return "中风险"
    # 否则返回低风险
    return "低风险"
  
  def generate_summary(self, analysis:Dict[str, Any]) -> str:
    """ 生成血糖分析摘要文本 """
    # 如果分析结果中包含错误信息，直接返回错误信息
    if analysis.get('error'):
      return str(analysis['error'])
    # 生成血糖分析摘要文本
    summary = (
      f"近{analysis['period_days']}天血糖概况：共记录{analysis['record_count']}次，"
      f"平均值{analysis['avg']} mmol/L，范围{analysis['min']}-{analysis['max']} mmol/L。"
      f"达标率{analysis['time_in_range']}%，趋势{analysis['trend']}。"
     )
    # 针对异常情况添加警示文案
    if analysis.get('low_count',0) > 0:
      summary += f"⚠️ 发生{analysis['low_count']}次低血糖，需关注。"
    if analysis.get('high_count',0) > 0:
      summary += f"⚠️ 发生{analysis['high_count']}次高血糖，注意控制饮食。"
    return summary

# 实例化单例对象
health_analyzer = HealthAnalyzer()
