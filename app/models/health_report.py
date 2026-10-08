from tortoise import fields, models

class HealthReport(models.Model):
  """
   健康报告表：由 AI 或系统生成的阶段性分析报告
   """
  id = fields.IntField(pk=True, description="主键ID")
  patient = fields.ForeignKeyField('models.Patient', related_name='health_reports', description="关联患者")
  report_type = fields.CharField(max_length=50, description="报告类型(周报/月报)")
  period_start = fields.DateField(description="统计开始日期")
  period_end = fields.DateField(description="统计结束日期")
  avg_blood_sugar = fields.FloatField(null=True, description="期间平均血糖")
  blood_sugar_std = fields.FloatField(null=True, description="血糖标准差(波动率)")
  time_in_range = fields.FloatField(null=True, description="达标时间占比(TIR)")
  summary = fields.TextField(description="健康总结")
  recommendations = fields.TextField(null=True, description="AI建议")
  risk_level = fields.CharField(max_length=20, default="低", description="风险等级")
  generated_at = fields.DatetimeField(auto_now_add=True, description="报告生成时间")

  class Meta:
    table = "health_reports"
