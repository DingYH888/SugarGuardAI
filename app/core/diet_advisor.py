"""饮食建议引擎：负责分析患者每日营养摄入情况，并根据血糖波动提供个性化食谱推荐。"""
import statistics 
from datetime import datetime, timedelta 
from typing import Dict, List, Optional 
from app.models.diet_record import DietRecord

class DietAdvisor:
  """ 饮食建议类，封装营养分析和食谱推荐逻辑 """
  async def get_daily_nutrition(self, patient_id: int,date_str:Optional[str] = None) -> Dict:
    """
     获取指定患者指定日期的营养摄入情况
     Args:
       patient_id: 患者ID
       date_str: 日期字符串，格式为YYYY-MM-DD，默认为当天
     Returns:
       Dict: 包含总热量、蛋白质、脂肪、碳水化合物的字典
     """
    # 如果传入日期字符串，则解析为日期对象
    if date_str:
      date = datetime.fromisoformat(date_str)
    else:
      date = datetime.now()

    # 将时间的时分秒清零，作为当天的起始时间
    start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
    # 起始时间 + 1天，作为当天的结束时间
    end_of_day = start_of_day + timedelta(days=1)
    # 查询指定日期和患者ID的饮食记录
    records = await DietRecord.filter(
      patient_id=patient_id,
      eaten_at__gte=start_of_day,
      eaten_at__lt=end_of_day
     ).all()
    
    # 计算总热量、蛋白质、脂肪、碳水化合物
    total_calories = sum(record.calories or 0 for record in records) # 总热量
    total_protein = sum(record.protein or 0 for record in records) # 总蛋白质
    total_fat = sum(record.fat or 0 for record in records) # 总脂肪
    total_carbs = sum(record.carbs or 0 for record in records) # 总碳水化合物

    # 提取所有不为空的 GI 值，用于计算当日饮食的平均升糖负荷水平
    gi_vals = [record.gi_value for record in records if record.gi_value is not None]
    # 如果有饮食数据则计算平均GI
    avg_gi = statistics.mean(gi_vals) if gi_vals else 0.0
    
    # 返回格式化后的汇总数据
    return {
      "date": date.strftime('%Y-%m-%d'), # 日期
      "meal_count": len(records), # 餐次
      'total_calories': round(total_calories, 1), # 总热量
      'total_protein': round(total_protein, 1), # 总蛋白质
      'total_fat': round(total_fat, 1), # 总脂肪
      'total_carbs': round(total_carbs, 1), # 总碳水化合物
      'avg_gi': avg_gi, # 平均GI
      "calorie_status": self._calorie_status(total_calories), # 热量状态
      "carb_status": self._carb_status(total_carbs), # 碳水化合物
      # 简化版记录列表，供前端快速展示，展示食物名称、热量、餐次
      "records": [
         {
          "name": record.food_name,
          "calories": record.calories,
          "meal": record.meal_type
         }
        for record in records
       ]
     }
  
  def _calorie_status(self, total_calories: float) -> str:
    """
     根据总热量判断饮食状态
     """
    if total_calories < 1200:
      return "热量摄入偏低，可能营养不足"
    if total_calories <= 1800:
      return "热量摄入适中，建议维持" 
    return "热量摄入偏高，可能营养过剩"
  
  def _carb_status(self, total_carbs: float) -> str:
    """
     根据总碳水化合物判断饮食状态
     """
    if total_carbs < 100:
      return "碳水化合物摄入偏低，可能营养不足"
    if total_carbs <= 200:
      return "碳水化合物摄入适中，建议维持"
    return "碳水化合物摄入偏高，注意控制碳水"

# 实例化单例对象
diet_advisor = DietAdvisor()
