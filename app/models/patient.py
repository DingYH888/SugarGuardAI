from tortoise import fields, models

class Patient(models.Model):
  """ 患者基础信息表 """
  id = fields.IntField(pk=True, description="主键ID")
  name = fields.CharField(max_length=50, description="患者姓名")
  age = fields.IntField(description="年龄")
  gender = fields.CharField(max_length=10, default="未知", description="性别")
  diabetes_type = fields.CharField(max_length=20, default="2型", description="糖尿病类型")
  diagnosis_date = fields.DateField(null=True, description="确诊日期")
  height = fields.FloatField(null=True, description="身高(cm)")
  weight = fields.FloatField(null=True, description="体重(kg)")
  phone = fields.CharField(max_length=20, null=True, description="联系电话")
  emergency_contact = fields.CharField(max_length=50, null=True, description="紧急联系人")
  emergency_phone = fields.CharField(max_length=20, null=True, description="紧急联系人电话")
  medical_history = fields.TextField(null=True, description="既往病史")
  allergies = fields.TextField(null=True, description="过敏史")
  created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
  updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

  class Meta:
    table = "patients"

  @property
  def bmi(self) -> float:
    """ 计算BMI : 体重(kg)/身高(m)的平方"""
    if self.weight and self.height:
      return round(self.weight / (self.height / 100) ** 2, 1)
    return 0.0
  
  @property
  def bmi_category(self) -> str:
    """ 计算BMI分类 """
    bmi_val = self.bmi
    if bmi_val < 18.5: return "偏瘦"
    if bmi_val < 24 : return "正常"
    return "肥胖"
