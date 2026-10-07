"""注册 Tortoise ORM 生命周期"""
from tortoise.contrib.fastapi import register_tortoise
from app.config import TORTOISE_ORM

# 注册数据库
def register_db(app):
  # 注册 Tortoise ORM
  # app: FastAPI实例
  # config: Tortoise ORM配置
  # generate_schemas: 是否生成数据库表结构
  register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
   )
