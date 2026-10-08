"""
对话历史记录模型。
"""
from tortoise import fields, models


class ChatHistory(models.Model):
  """
   对话历史表:存储患者与AI助手之间的聊天记录。
   """
  id = fields.IntField(pk=True, description="主键ID")
  patient = fields.ForeignKeyField('models.Patient',related_name='chat_histories',description="关联患者")
  role = fields.CharField(max_length=20, description="角色(user/assistant)")
  content = fields.TextField(description="对话内容")
  created_at = fields.DatetimeField(auto_now_add=True, description="发送时间")

  class Meta:
    table = "chat_history"
