"""
对话相关请求与响应 Schema。
"""
from datetime import datetime
from pydantic import BaseModel

class ChatMessage(BaseModel):
  """
   客户端发送消息时的请求体
   """
  patient_id: int # 患者ID
  message: str  # 消息内容

class ChatResponse(BaseModel):
  """
   服务端响应消息时的响应体
   """
  id:int
  patient_id: int   # 患者ID
  user_message: str  # 用户输入的文本
  ai_response: str  # AI回复的文本
  created_at: datetime

class ChatHistoryResponse(BaseModel):
  """
   对话历史记录响应体
   """
  id:int
  patient_id:int
  role:str
  content:str
  created_at:datetime
