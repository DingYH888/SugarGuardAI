from typing import List, Optional
from app.core.knowledge_base import search_knowledge

class RAGEngine:
  """ 糖尿病RAG引擎 """
  def retrieve(
    self, 
    query: str, 
    category: Optional[str] = None,
    top_k: int = 5,
    min_score: float = 0.3,  #最低相似度
   ) -> str:
    """
     检索知识库
     query: 用户问题
     category: 知识库分类，如“血糖管理”
     top_k: 返回的最相思文档数量
     min_score: 最小相似度阈值，低于该值的结果被过滤
     """
    # 检索知识库
    raw_docs = search_knowledge(query=query, category=category, top_k=top_k)
    docs = [doc for doc in raw_docs if doc["score"] >= min_score]
    return self._build_context(docs)
  
  def _build_context(self, knowlegde_docs: List[dict]) -> str:
    """
     将检索结果列表格式化为带编号的引用字符串
     格式： [参考1](分类|来源：xxx)\n文档内容正文
     """
    if not knowlegde_docs:
      return "暂无相关参考知识"
    # 初始化引用列表
    parts: List[str] = []
    # 遍历检索结果
    for i, doc in enumerate(knowlegde_docs, start=1):
      meta = doc["metadata"] or {}
      category = meta.get("category", "未分类")
      source = meta.get("source", "未知来源")
      parts.append(f"[参考{i}]({category} | 来源：{source})\n{doc['content']}")
    return "\n\n".join(parts)

# 单例实例
rag_engine = RAGEngine()
