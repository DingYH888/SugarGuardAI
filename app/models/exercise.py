from tortoise import fields, models

class Exercise(models.Model):
  """
   运动记录表：记录运动项目及运动前后的血糖对比
   """
  id = fields.IntField(pk=True, description="主键ID")
  patient = fields.ForeignKeyField('models.Patient', related_name='exercises', description="关联患者")
  exercise_type = fields.CharField(max_length=50, description="运动类型")
  duration_min = fields.IntField(description="时长(分钟)")
  intensity = fields.CharField(max_length=20, default="中等", description="运动强度")
  calories_burned = fields.FloatField(null=True, description="消耗热量")
  performed_at = fields.DatetimeField(description="运动时间")
  blood_sugar_before = fields.FloatField(null=True, description="运动前血糖")
  blood_sugar_after = fields.FloatField(null=True, description="运动后血糖")
  note = fields.TextField(null=True, description="备注")
  created_at = fields.DatetimeField(auto_now_add=True, description="记录时间")

  class Meta:
    table = "exercise_records"

  @property
  def bs_change(self) -> float:
    """计算运动前后的血糖变化值"""
    if self.blood_sugar_before is not None and self.blood_sugar_after is not None:
      return round(self.blood_sugar_after - self.blood_sugar_before, 1)
    return 0.0
