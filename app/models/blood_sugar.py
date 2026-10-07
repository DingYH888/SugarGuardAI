from tortoise import fields, models

class BloodSugar(models.Model):
  """
   血糖记录表：记录不同时段的血糖测量值
   """
  id = fields.IntField(pk=True, description="主键ID")
  # 关联患者表，一对多关系
  patient = fields.ForeignKeyField('models.Patient', related_name='blood_sugars', description="关联患者")
  value = fields.FloatField(description="血糖值(mmol/L)")
  measure_type = fields.CharField(max_length=20, description="测量类型(空腹/餐后2h/睡前等)")
  measured_at = fields.DatetimeField(description="测量时间")
  note = fields.TextField(null=True, description="备注说明")
  created_at = fields.DatetimeField(auto_now_add=True, description="录入时间")

  class Meta:
    table = "blood_sugar"

  @property
  def status(self) -> str:
    """根据血糖值判断健康状态"""
    if self.value < 3.9: return "低血糖"
    if self.value <= 7.0: return "正常"
    if self.value <= 10.0: return "偏高"
    return "高血糖"
