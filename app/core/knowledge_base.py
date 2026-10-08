"""
医学知识库的初始化与检索。
"""
from typing import Any, Dict, List, Optional
from app.core.vector_store import vector_store

# 糖尿病医学知识库
DIABETES_KNOWLEDGE: List[Dict[str, str]] = [
   {
    "content": "糖尿病患者空腹血糖控制目标为4.4-7.0 mmol/L，餐后2小时血糖<10.0 mmol/L。血糖<3.9 mmol/L为低血糖，需要立即处理。",
    "category": "血糖管理",
    "source": "中国2型糖尿病防治指南",
   },
   {
    "content": "低血糖症状：心悸、出汗、饥饿感、手抖、头晕、视物模糊。严重时可出现意识障碍。处理：立即口服15g葡萄糖或含糖饮料，15分钟后复测血糖。",
    "category": "低血糖",
    "source": "糖尿病低血糖诊治指南",
   },
   {
    "content": "高血糖症状：口渴、多饮、多尿、乏力、视力模糊。空腹血糖>13.9 mmol/L时需警惕酮症酸中毒。",
    "category": "高血糖",
    "source": "中国2型糖尿病防治指南",
   },
   {
    "content": "糖化血红蛋白(HbA1c)反映近2-3个月平均血糖水平，目标<7.0%。每3个月检测一次。",
    "category": "血糖监测",
    "source": "ADA糖尿病诊疗标准",
   },
   {
    "content": "糖尿病患者每日碳水化合物应占总热量的45-60%，优选低GI食物（GI<55）。推荐全谷物、豆类、蔬菜。",
    "category": "饮食管理",
    "source": "糖尿病医学营养治疗指南",
   },
   {
    "content": "低GI食物推荐：燕麦(GI 55)、糙米(GI 56)、红薯(GI 54)、苹果(GI 36)、梨(GI 38)、扁豆(GI 32)、西兰花(GI 15)。",
    "category": "饮食管理",
    "source": "中国食物成分表",
   },
   {
    "content": "高GI食物应避免：白米饭(GI 83)、白面包(GI 75)、西瓜(GI 72)、土豆泥(GI 85)、糯米(GI 87)。",
    "category": "饮食管理",
    "source": "中国食物成分表",
   },
   {
    "content": "糖尿病患者每日膳食纤维推荐25-30g，有助于控制血糖和改善肠道健康。推荐来源：蔬菜、全谷物、豆类。",
    "category": "饮食管理",
    "source": "糖尿病医学营养治疗指南",
   },
   {
    "content": "糖尿病患者每日蛋白质摄入0.8-1.0g/kg体重，肾病患者需限制在0.6-0.8g/kg。优选优质蛋白：鱼、禽、蛋、豆制品。",
    "category": "饮食管理",
    "source": "糖尿病肾病诊疗指南",
   },
   {
    "content": "糖尿病患者应限制钠盐摄入<5g/天，有助于控制血压。减少腌制食品、加工食品的摄入。",
    "category": "饮食管理",
    "source": "中国2型糖尿病防治指南",
   },
   {
    "content": "糖尿病患者推荐每周至少150分钟中等强度有氧运动（如快走、骑车、游泳），分5天进行，每次30分钟。运动可改善胰岛素敏感性。",
    "category": "运动管理",
    "source": "ADA糖尿病诊疗标准",
   },
   {
    "content": "运动注意事项：血糖>13.9 mmol/L或<5.6 mmol/L时不宜运动。运动前测血糖，随身携带糖果。避免空腹运动。运动后注意迟发性低血糖。",
    "category": "运动管理",
    "source": "中国2型糖尿病防治指南",
   },
   {
    "content": "推荐运动类型：有氧运动（快走、游泳、骑车）+抗阻训练（哑铃、弹力带）。每周2-3次抗阻训练，每次8-10个动作。",
    "category": "运动管理",
    "source": "ADA糖尿病诊疗标准",
   },
   {
    "content": "二甲双胍是2型糖尿病一线用药，可降低HbA1c 1.0-1.5%。常见副作用为胃肠道反应，建议餐后服用。禁用于肾功能不全(eGFR<30)。",
    "category": "用药管理",
    "source": "中国2型糖尿病防治指南",
   },
   {
    "content": "磺脲类药物（格列美脲、格列齐特）可降低HbA1c 1.0-1.5%，主要副作用为低血糖和体重增加。老年人需减量。",
    "category": "用药管理",
    "source": "中国2型糖尿病防治指南",
   },
   {
    "content": "胰岛素使用注意事项：注射部位轮换（腹部>大腿>上臂），注射后30分钟内进食，注意低血糖预防。基础胰岛素一般睡前注射。",
    "category": "用药管理",
    "source": "胰岛素使用指南",
   },
   {
    "content": "SGLT-2抑制剂（达格列净、恩格列净）有心肾保护作用，适合合并心血管疾病或肾病的糖尿病患者。注意泌尿生殖系统感染风险。",
    "category": "用药管理",
    "source": "ADA糖尿病诊疗标准",
   },
   {
    "content": "糖尿病视网膜病变：每年眼底检查。早期无症状，晚期可致失明。血糖、血压控制是预防关键。",
    "category": "并发症",
    "source": "中国2型糖尿病防治指南",
   },
   {
    "content": "糖尿病肾病：定期检测尿微量白蛋白/肌酐比值(UACR)和eGFR。早期干预可延缓进展。控制血糖、血压、血脂。",
    "category": "并发症",
    "source": "糖尿病肾病诊疗指南",
   },
   {
    "content": "糖尿病足：每日检查双脚，保持清洁干燥，穿合适鞋袜，避免赤脚走路。发现伤口不愈合及时就医。",
    "category": "并发症",
    "source": "中国2型糖尿病防治指南",
   },
   {
    "content": "糖尿病神经病变：四肢麻木、疼痛、感觉异常。控制血糖是根本。可使用甲钴胺、硫辛酸等营养神经药物。",
    "category": "并发症",
    "source": "中国2型糖尿病防治指南",
   },
]

def init_knowledge_base() -> None:
  """
   初始化医学知识库：将医学知识库中的文档导入 ChromaDB
   """
  if vector_store.count() > 0:
    # 知识库已有数据，跳过本次初始化，防止重复导入
    return
  
  # 提取content字段作为文档文本
  documents = [item["content"] for item in DIABETES_KNOWLEDGE]
  # 构造metadatas，携带 category 和 source
  metadatas: List[Dict[str, Any]] = [
     {"category": item["category"], "source": item["source"]}
    for item in DIABETES_KNOWLEDGE
   ]
  # 使用顺序编号作为固定ID，便于后续定位和更新文档
  ids = [f"doc_{i}" for i in range(len(DIABETES_KNOWLEDGE))]

  # 写入向量库
  vector_store.add_documents(documents=documents, metadatas=metadatas, ids=ids)

  print("知识库初始化完成，文档数量：", vector_store.count())


def search_knowledge(
  query: str, 
  category: Optional[str] = None,
  top_k: int = 5) -> List[Dict]:
  """
   检索与查询语句最相关的知识库文档
   query: 用户问题
   category: 知识库分类，可选值：血糖管理、低血糖、高血糖、血糖监测、饮食管理、运动管理、用药管理、并发症
   top_k: 返回的文档数量，默认返回5条
   """

  # 将字符串category转换成 ChromaDB 要求的字典格式
  where: Optional[Dict[str, str]] = {"category": category} if category else None
  # 查询向量数据库
  results = vector_store.query(query_text=query, top_k=top_k, where=where)

  # 获取文档内容、元数据、余弦距离
  docs = results.get("documents") or []
  metas = results.get("metadatas") or []
  dists = results.get("distances") or []

  # 初始化输出列表
  out: List[Dict] = []
  # 遍历文档内容
  for i in range(len(docs)):
    # 将余弦距离转为 0~1 相似度分数
    score = 0.0
    if i < len(dists) and dists[i] is not None:
      # 余弦距离越小，相似度越高，如果距离是0.1，分数就是0.9（非常像）
      score = max(0.0,1.0-float(dists[i]))

      # 获取对于的元数据
      meta = metas[i] if i < len(metas) else {}
      # 构建输出字典
      out.append({
        "content": docs[i],
        "metadata": meta or {},
        "score": score,
       })
  # 返回结果
  return out
