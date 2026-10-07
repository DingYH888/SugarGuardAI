from tortoise import fields, models

class Medication(models.Model):
  """
   用药记录表：管理患者的口服药或胰岛素方案
   """
  id = fields.IntField(pk=True, description="主键ID")
  patient = fields.ForeignKeyField('models.Patient', related_name='medications', description="关联患者")
  drug_name = fields.CharField(max_length=100, description="药品名称")
  drug_type = fields.CharField(max_length=50, null=True, description="药物类型(口服/注射)")
  dosage = fields.CharField(max_length=50, description="单次剂量")
  frequency = fields.CharField(max_length=50, null=True, description="频率(如:每日2次)")
  timing = fields.TextField(null=True, description="用药时机(如:餐前30分)")
  start_date = fields.DateField(description="开始用药日期")
  end_date = fields.DateField(null=True, description="停药日期")
  is_active = fields.BooleanField(default=True, description="是否正在服用")
  side_effects = fields.TextField(null=True, description="副作用记录")
  note = fields.TextField(null=True, description="用药备注")
  created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

  class Meta:
    table = "medications"
