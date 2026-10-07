import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DB_HOST = os.getenv('DB_HOST',"localhost")
DB_PORT = os.getenv('DB_PORT',"3306")
DB_USER = os.getenv('DB_USER',"root")
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME',"diabetes")

# 密码 URL 编码处理
_encoded_password = quote_plus(DB_PASSWORD)

# 数据库连接 URL
DATABASE_URL = (
  f"mysql://{DB_USER}:{_encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
  f"?charset=utf8mb4"
)

# Tortoise ORM 配置
TORTOISE_ORM = {
  "connections": {
    "default": DATABASE_URL
   },
  "apps": {
    "models": {
      "models": ["app.models"],
      "default_connection": "default",
     }
   }
}
