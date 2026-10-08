"""
ChromaDB 向量数据库。

负责医学知识文档的向量嵌入存储与语义检索。
每个文档由 content（文本内容）、metadata（分类/来源）和 embedding（语义向量）组成。
查询时根据用户问题与文档向量的余弦相似度返回 top_k 条最相关内容。
"""
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
import chromadb
import os
from langchain_huggingface import HuggingFaceEmbeddings

# 加载环境变量
load_dotenv()

class VectorStore:
  """
   ChromaDB 向量数据库管理器。
   """
  def __init__(self):
    # 获取环境变量
    chroma_persist_dir = os.getenv("CHROMA_PERSIST_DIR")
    chroma_collection_name = os.getenv("CHROMA_COLLECTION_NAME")
    
    # 创建本地存储目录，递归创建，忽略已存在错误
    Path(chroma_persist_dir).mkdir(parents=True, exist_ok=True)
    # 实例化持久化客户端
    self.client = chromadb.PersistentClient(path=chroma_persist_dir)

    # 设置中文词嵌入模型
    self.embeddings = HuggingFaceEmbeddings(
      model_name="paraphrase-multilingual-MiniLM-L12-v2",
      encode_kwargs={"normalize_embeddings": True},
     )

    # 获取或创建集合
    self.collection = self.client.get_or_create_collection(
      # 集合名
      name=chroma_collection_name,
      # 数据库没补使用的hnsw索引算法，使用余弦相似度计算文档相似度
      metadata={"hnsw:space": "cosine"},
     )

  def add_documents(
    self,
    documents: List[str],
    metadatas: Optional[List[Dict[str, Any]]] = None,
    ids: Optional[List[str]] = None
   ) -> None:
    """
     向向量库批量添加文档
     documents: 要存入的纯文本列表
     metadatas: 每个文档的元数据
     ids: 文档的唯一标志列表
     """
    # 未提供IDs时，以文档内容的 MD5 哈希值作为ID
    # 由于同样的文字内容，生成的 MD5 哈希值是唯一的，因此可以确保文档的唯一性
    if ids is None:
      ids = [hashlib.md5(document.encode("uft-8")).hexdigest() for document in documents]
    
    # 生成语义向量
    embeddings = self.embeddings.embed_documents(documents)

    # 分批处理，没批处理100个文档
    batch_size = 100
    for i in range(0, len(documents), batch_size):
      # 将文档和向量添加到集合
      self.collection.add(
         # 切片取出当前批次的 100 条文档
        documents = documents[i:i+batch_size],
        # 取出当前批次的100条语义向量
        embeddings = embeddings[i:i+batch_size],
        # 取出当前批次的100条元数据
        metadatas = metadatas[i:i+batch_size],
        # 取出当前批次的100条文档ID
        ids = ids[i:i+batch_size]
       )
      
  def delete(self, ids: List[str]) -> None:
    """
     根据文档ID批量删除文档
     """
    self.collection.delete(ids=ids)
    

  def count(self) -> int:
    """
     返回向量库中文档的总数量，用于判断知识库是否已经初始化
     """
    return int(self.collection.count())
  
  def query(
    self,
    query_text: str,
    top_k: Optional[int] = None,
    where: Optional[Dict] = None,
   ) -> Dict:
    """
     语义检索：返回与查询文本最相似的 top_k 条文档
     query_text: 查询文本
     top_k: 返回的文档数量
     where: ChromaDB 元数据过滤条件，例如：{"来源":"医疗期刊"}
     """
    top_k = top_k or os.getenv("RAG_TOP_K")

    # 生成语义向量
    query_embedding = self.embeddings.embed_query(query_text)

    # 查询集合
    results = self.collection.query(
      query_embeddings=[query_embedding],  # 单个查询向量
      n_results=top_k,           # 返回的文档数量，默认10条
      where=where,            # 元数据过滤条件
      include=["documents", "metadatas", "distances"], # 返回的字段：文档内容、元数据和余弦距离
     )
    # ChromaDB返回类似 {"documents": [["结果1", "结果2"]]} 这种格式，需要进行脱壳处理。
    return {
      "documents": results["documents"][0] if results.get("documents") else [],
      "metadatas": results["metadatas"][0] if results.get("metadatas") else [],
      "distances": results["distances"][0] if results.get("distances") else [],
     }
  
# 单例实例
vector_store = VectorStore()
