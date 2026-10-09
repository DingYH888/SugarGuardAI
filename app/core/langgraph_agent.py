"""
LangGraph Agent 工作流编排模块。
流程：意图识别 → 从数据库获取患者档案 → 知识库检索 → 调用LLM生成建议 → 风险评估与警告追加
"""
from typing import Dict, Optional, TypedDict
from langgraph.graph import END, StateGraph
from app.core.health_analyzer import health_analyzer
from app.core.llm_client import llm_client
from app.core.rag_engine import rag_engine
from app.models.patient import Patient

class AgentState(TypedDict , total = False):
  """
   LangGraph 流水线中各节点共享的状态结构
   total=False 不强制要求全部填充，未赋值字段默认为None
   """
  # 患者id
  patient_id: int
  # 意图：blood_sugar(血糖) / diet_query(饮食) / medication_query(用药) / health_query(其他)
  input_type: str
  # 用户消息
  user_message : str
  # 患者档案
  patient_context: str
  # health_analyzer结构化结果
  blood_sugar_data: Optional[Dict] = None
  # RAG检索结果
  rag_context: str
  # LLM生成建议(不包含风险追加文案)
  recommendations: str
  # 风险等级: 高/中/低
  risk_level: str
  # 最终回复：建议+风险警告
  response: str

async def classify_input(state: AgentState) -> AgentState:
  """
   意图识别节点
   """
  # 获取用户消息
  message = state['user_message'].lower().strip()
  # 匹配关键词
  if any(keyword in message for keyword in ['血糖', 'mmol', '测量', '记录血糖']):
    input_type = 'blood_sugar'
  elif any(keyword in message for keyword in ['饮食', '吃', '食物', '食谱','营养','能吃什么']):
    input_type = 'diet_query'
  elif any(keyword in message for keyword in ['用药', '药', '胰岛素', '打针', '二甲双胍']):
    input_type = 'medication_query'
  else:
    input_type = 'health_query'
  state['input_type'] = input_type
  return state

async def load_patient_context(state: AgentState) -> AgentState:
  """
   获取患者档案
   """
  # 获取患者信息
  patient_id = state['patient_id']
  patient = await Patient.get_or_none(id=patient_id)
  if patient:
    # 调用 health_analyzer 获取该患者近7天的血糖统计
    bg_analysis = await health_analyzer.analyze_blood_sugar(patient_id,days=7)
    # 将统计结果转为文本
    bg_summary = health_analyzer.generate_summary(bg_analysis)

    context = f"""患者信息:
     - 姓名:{patient.name},年龄:{patient.age}岁,性别:{patient.gender}
     - 糖尿病类型：{patient.diabetes_type}
     - BMI:{patient.bmi}({patient.bmi_category})
     - 病史:{patient.medical_history or '无特殊'}
     - 过敏:{patient.allergies or '无'}
     - 近7天血糖概况:{bg_summary}"""

    # 将患者情况写入状态
    state['patient_context'] = context
    # 将血糖统计结果写入状态
    state['blood_sugar_data'] = bg_analysis
  else:
    state['patient_context'] = "(未找到患者档案)"
  
  return state

async def retrieve_knowledge(state: AgentState) -> AgentState:
  """
   知识库检索
   """
  # 获取用户意图
  input_type = state.get("input_type","")

  if input_type == "health_query":
    # 通用健康知识检索，不限制分类，检索全量知识库
    state['rag_context'] = rag_engine.retrieve(
      query=state['user_message'],
      category=None
     )
  else:
    # 根据意图检索相关文档
    _INTENT_CATEGORY_MAP = {
      "blood_sugar": "血糖管理",
      "diet_query": "饮食管理",
      "medication_query": "用药管理",
     }
    category = _INTENT_CATEGORY_MAP.get(input_type, "")
    state['rag_context'] = rag_engine.retrieve(
      query=state['user_message'],
      category=category
     )
  print(state['rag_context'])
  return state

async def analyze_and_generate(state: AgentState) -> AgentState:
  """
   生成节点：组合患者信息 + RAG检索结果,调用LLM生成个性化建议
   """
  system_prompt = f"""你是糖尿病健康管理AI助手。请根据以下信息为患者提供个性化建议。
   {state.get('patient_context', '')}
  
   相关医学知识：
   {state.get('rag_context', '')}
   请提供：
   1. 对患者当前状况的分析
   2. 具体可执行的建议
   3. 需要注意的事项

   请用温和关怀的语气，给出简洁实用的建议。"""

  # 调用LLM生成建议
  response = llm_client.chat(
    system_prompt=system_prompt,
    user_message=state['user_message'],
   )

  # 将建议写入状态
  state['recommendations'] = response
  return state

async def risk_assessment(state: AgentState) -> AgentState:
  """
   风险评估节点:根据血糖统计的risk_level在回复末尾追加风险警告
   """
  # 获取血糖统计结果
  bg_data = state.get('blood_sugar_data', {})
  # 获取风险等级
  risk_level = bg_data.get('risk_level') or "低风险"
  # 将风险等级写入状态
  state['risk_level'] = risk_level
  # 根据风险等级生成警告
  warning = ""
  if risk_level == "高风险":
    warning = "\n\n⚠️ **高风险警告**：您的血糖控制不理想，建议尽快联系主治医生调整治疗方案。"
  elif risk_level == "中风险":
    warning = "\n\n⚡ **提醒**：近期血糖波动较大，请注意饮食和用药规律。"
  # 将警告追加到 LLM 生成的建议末尾
  state["response"] = (state.get('recommendations', '') + warning)

  return state

def create_agent_workflow():
  """
   创建 LangGraph 工作流
   """
  # 创建工作流图
  workflow = StateGraph(AgentState)
  # 添加节点
  workflow.add_node("classify", classify_input)
  workflow.add_node("load_context", load_patient_context)
  workflow.add_node("retrieve", retrieve_knowledge)
  workflow.add_node("generate", analyze_and_generate)
  workflow.add_node("assess_risk", risk_assessment)

  # 串联节点：意图识别 → 获取患者档案 → 知识库检索 → 生成建议 → 风险评估
  workflow.set_entry_point("classify")
  workflow.add_edge("classify", "load_context")
  workflow.add_edge("load_context", "retrieve")
  workflow.add_edge("retrieve", "generate")
  workflow.add_edge("generate", "assess_risk")
  workflow.add_edge("assess_risk", END)

  # 编译工作流
  return workflow.compile()

# 实例化单例对象
agent_app = create_agent_workflow()

async def run_agent(patient_id: int, user_message: str) -> Dict:
  """
   对外服务： 接收患者ID和用户消息，调用完整工作流并返回结果
   """
  # 创建初始状态
  initial_state = AgentState = {
    "patient_id": patient_id,
    "user_message": user_message,
    "input_type": "",
    "patient_context": "",
    "blood_sugar_data": None,
    "rag_context": "",
    "recommendations": "",
    "risk_level": "",
    "response": ""
   }
  # 执行工作流
  result = await agent_app.ainvoke(initial_state)
  return {
    "response": result['response'] or "",
    "risk_level": result['risk_level'] or "",
    "input_type": result['input_type'] or "",
    "blood_sugar_data": result['blood_sugar_data']
   }
