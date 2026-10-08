"""LLM 大模型客户端封装"""
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# 加载环境变量
load_dotenv()

class LLMClient:
  """LLM 大模型客户端"""
  def __init__(self) -> None:
    """ 初始化LLM客户端 """
    # 加载环境变量
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL")
    base_url = os.getenv("LLM_BASE_URL")
    temperature = os.getenv("LLM_TEMPERATURE")
    max_tokens = os.getenv("LLM_MAX_TOKENS")
    # 初始化模型实例
    self._llm = ChatOpenAI(
      model=model,
      openai_api_key=api_key,
      openai_api_base=base_url,
      temperature=temperature,
      max_tokens=max_tokens
     )

  """
   核心对话方法
   system_prompt：系统提示词
   user_message：用户提示词
   chat_history：对话历史
   """
  def chat(self,system_prompt:str,user_message:str,chat_history:Optional[List[Dict]] = None) -> str:
    # 1.构建消息列表，添加系统提示词
    messages = [SystemMessage(content=system_prompt)]
    # 2.添加对话历史
    if chat_history:
      # 仅取最近 10 条对话记录，避免token消耗过大且防止上下文偏移
      for msg in chat_history[-10:]:
        role = msg.get("role")
        content = msg.get("content")
        # 添加用户消息
        if role == "user":
          messages.append(HumanMessage(content=content))
        # 添加模型消息
        elif role in ("assistant","bot"):
          messages.append(AIMessage(content=content))
    # 3.加入当前用户的问题
    messages.append(HumanMessage(content=user_message))
    # 4.调用模型生成响应结果
    try:
      response = self._llm.invoke(messages)
      # 返回模型生成的文本内容
      return str(response.content)
    except Exception as e:
      return f"抱歉，医学助手暂时无法响应，请稍后再试或咨询医生。错误信息: {e}"

# 实例化单例对象
llm_client = LLMClient()
