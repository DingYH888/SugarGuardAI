"""饮食建议引擎：负责分析患者每日营养摄入情况，并根据血糖波动提供个性化食谱推荐。"""
import statistics 
from datetime import datetime, timedelta 
from typing import Dict, List, Optional 
from app.models.diet_record import DietRecord

# 定义静态的糖尿病推荐食谱库
RECOMMENDED_FOODS: List[Dict] = [
   {"name": "燕麦粥", "calories": 150, "carbs": 27, "protein": 5, "fat": 3, "gi": 55, "meal": "早餐", "tip": "富含膳食纤维，升糖慢"},
   {"name": "水煮鸡蛋", "calories": 78, "carbs": 0.6, "protein": 6, "fat": 5, "gi": 0, "meal": "早餐", "tip": "优质蛋白质，几乎不含碳水"},
   {"name": "全麦面包", "calories": 246, "carbs": 41, "protein": 13, "fat": 3, "gi": 51, "meal": "早餐", "tip": "比白面包GI低很多"},
   {"name": "清蒸鱼", "calories": 120, "carbs": 0, "protein": 20, "fat": 4, "gi": 0, "meal": "午餐/晚餐", "tip": "优质蛋白+omega-3脂肪酸"},
   {"name": "糙米饭", "calories": 220, "carbs": 46, "protein": 5, "fat": 2, "gi": 56, "meal": "午餐/晚餐", "tip": "比白米GI低，营养更丰富"},
   {"name": "西兰花", "calories": 34, "carbs": 7, "protein": 3, "fat": 0.4, "gi": 15, "meal": "午餐/晚餐", "tip": "低GI蔬菜，富含维C"},
   {"name": "苦瓜", "calories": 17, "carbs": 3.7, "protein": 1, "fat": 0.2, "gi": 24, "meal": "午餐/晚餐", "tip": "传统降糖食材"},
   {"name": "豆腐", "calories": 76, "carbs": 1.9, "protein": 8, "fat": 4.8, "gi": 15, "meal": "午餐/晚餐", "tip": "植物蛋白，低GI"},
   {"name": "苹果", "calories": 52, "carbs": 14, "protein": 0.3, "fat": 0.2, "gi": 36, "meal": "加餐", "tip": "低GI水果，适量食用"},
   {"name": "无糖酸奶", "calories": 63, "carbs": 4.7, "protein": 5, "fat": 2, "gi": 27, "meal": "加餐", "tip": "益生菌+蛋白质"},
]

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

  def recommend_meal(self, meal_type: str, recent_bg: Optional[float] = None) -> List[Dict]:
    """
     根据当前餐次和近期血糖水平推荐餐食
     :param meal_type: 想要查询的餐次（早餐/午餐/晚餐）
     :param recent_bg: 最近一次测量的血糖值
     """
    # 从食谱库中初步筛选：匹配餐次，或者标记为“加餐”的通用食物
    suitable = [f for f in RECOMMENDED_FOODS if meal_type in f["meal"] or f["meal"] == "加餐"]
    
    # 针对糖尿病的个性化逻辑：如果血糖高于 8.0 mmol/L（控制不佳）
    if recent_bg and recent_bg > 8.0:
      # 将候选食物按照 GI 值从低到高排序，并只取前 4 个升糖最慢的
      suitable = sorted(suitable, key=lambda x: x["gi"])[:4]
    # 如果血糖正常或未提供血糖值
    else:
      # 默认取库中的前 5 个建议
      suitable = suitable[:5]
      
    return suitable # 返回推荐食物列表
  
# 实例化单例对象
diet_advisor = DietAdvisor()
