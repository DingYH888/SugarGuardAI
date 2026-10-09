""" FastAPI 应用入口文件 """
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.knowledge_base import init_knowledge_base
from app.routers import main_router
from app.database import register_db
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
  """应用生命周期管理：启动时初始化向量知识库。"""
  init_knowledge_base()
  yield

# 创建FastAPI实例
app = FastAPI(lifespan=lifespan)

# 添加CORS中间件
app.add_middleware(
  CORSMiddleware,
  # 允许跨域的前端地址
  allow_origins=["*"],
  # 允许携带Cookie
  allow_credentials=True,
  # 允许的请求方法
  allow_methods=["*"],
  # 允许的请求头
  allow_headers=["*"],
)
# 注册路由
app.include_router(main_router)
# 注册数据库
register_db(app)

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
