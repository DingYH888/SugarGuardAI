"""
AI 对话路由
"""
from this import d
from typing import List
from fastapi import APIRouter
from app.core.langgraph_agent import run_agent
from app.models.chat_history import ChatHistory
from app.schemas.chat import ChatHistoryResponse, ChatMessage, ChatResponse

router = APIRouter(prefix="/chat",tags=["chat"])

@router.post("/message",response_model=ChatResponse)
async def send_message(data:ChatMessage):
  """
   对话接口
   """
  # 1.持久化用户消息
  user_msg = await ChatHistory.create(
    patient_id = data.patient_id,
    role="user",
    content=data.message
   )

  # 2.触发 LangGraph 工作流
  result = await run_agent(data.patient_id,data.message)

  # 3.持久化AI回复
  ai_msg = await ChatHistory.create(
    patient_id = data.patient_id,
    role="assistant",
    content=result["response"]
   )

  # 4.构造响应体
  return ChatResponse(
    id = ai_msg.id,
    patient_id=data.patient_id,
    user_message=data.message,
    ai_response=result["response"],
    created_at=ai_msg.created_at
   )

@router.get("/history/{patient_id}",response_model=List[ChatHistoryResponse])
async def get_history(patient_id:int,limit:int=50):
  """
   获取患者的历史对话记录
   """
  records = (
    await ChatHistory.filter(patient_id=patient_id)
     .order_by("-created_at")
     .limit(limit)
   )
  return records
