<div align="center">

# 🩺 SugarGuardAI —— 智能慢性病管理系统

**基于 LLM 大模型 · Agent · RAG · LangGraph · LangChain 构建的 AI 智能健康管理平台**

为糖尿病患者提供 **7×24 小时** 个性化健康监测、饮食指导、用药管理、运动规划与 AI 健康咨询服务。

</div>

---

## 📖 项目简介

`SugarGuardAI` 是一款面向慢性病（以糖尿病为核心）人群的智能健康管理助手。系统融合大语言模型（LLM）、智能体（Agent）、检索增强生成（RAG）等前沿 AI 技术，结合患者实时健康数据与医学知识库，为每位用户量身定制个性化健康管理方案。

---

## ✨ 核心功能

| 功能模块 | 说明 |
| :--- | :--- |
| 📊 仪表盘 | 患者健康数据总览，指标趋势可视化 |
| 🩸 血糖管理 | 血糖记录、统计分析与异常风险预警（高中低风险等级） |
| 🥗 饮食管理 | 饮食记录、每日营养统计与 AI 个性化饮食推荐 |
| 💊 用药管理 | 用药记录、智能提醒与用药方案管理 |
| 🏃 运动管理 | 运动记录与科学运动方案规划 |
| 📈 健康报告 | AI 自动生成周报 / 月报，含血糖分析总结与医学建议 |
| 🤖 AI 健康咨询 | 7×24 小时智能健康问答助手（LangGraph Agent 驱动） |
| 👤 患者管理 | 患者档案的增删改查 |

---

## 🧠 AI 能力

项目内置完整的 AI 应用编排架构：

1. **LangGraph Agent 工作流** —— 意图识别 → 读取患者档案 → RAG 知识检索 → LLM 生成建议 → 风险评估与警告追加（`app/core/langgraph_agent.py`）
2. **RAG 医学知识库** —— 内嵌糖尿病医学知识，基于 ChromaDB 向量检索（`app/core/knowledge_base.py`、`rag_engine.py`）
3. **向量嵌入** —— 中文语义向量模型 `bge-large-zh-v1.5`（ModelScope 下载，本地推理）
4. **大模型调用** —— 阿里云百炼 qwen 系列（OpenAI 兼容接口）

---

## 🛠️ 技术选型

| 分类 | 技术 / 工具 | 说明 |
| :--- | :--- | :--- |
| 开发操作系统 | ![Windows](https://img.shields.io/badge/Windows-11-0078D6?logo=windows&logoColor=white) | Windows 11 |
| 开发工具 | VSCode | 主开发环境 |
| Python 版本 | ![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | 3.12 |
| 项目管理工具 | uv | 高速 Python 包管理器 |
| 数据库 | MySQL 8 + DataGrip | 关系型数据存储与可视化管理 |
| Web 框架 | FastAPI | 高性能异步 API 框架 |
| 服务器 | Uvicorn | ASGI 服务器 |
| ORM 框架 | Tortoise-ORM | 异步 ORM |
| AI 应用编排 | LangGraph | Agent 工作流编排 |
| 向量数据库 | ChromaDB | RAG 知识检索 |
| 大模型调用 | LangChain + 阿里云百炼 qwen | LLM 接入与链式调用（OpenAI 兼容） |
| 向量嵌入 | sentence-transformers + bge-large-zh-v1.5 | 中文语义向量模型（ModelScope 下载） |
| 前端框架 | Vue 3 + TypeScript | 响应式前端 + 类型安全 |
| 前端 UI | Element Plus + ECharts | 组件库与数据可视化 |

---

## 🚀 快速开始

### 1️⃣ 克隆仓库

```bash
git clone https://github.com/DingYH888/SugarGuardAI.git
cd SugarGuardAI
```

### 2️⃣ 环境准备

- Python `3.12`
- Node.js `>= 18`
- MySQL `8.x`
- [uv](https://docs.astral.sh/uv/) 包管理器

### 3️⃣ 数据库准备

在 MySQL 中创建数据库：

```sql
CREATE DATABASE diabetes DEFAULT CHARACTER SET utf8mb4;
```

### 4️⃣ 后端配置

```bash
# 安装依赖
uv sync

# 新建环境变量文件（已加入 .gitignore）
# 内容见下方「环境变量说明」，填入数据库连接、LLM API Key 等
```

### 5️⃣ 下载 Embedding 模型

向量检索依赖中文语义向量模型，需从 ModelScope 下载到本地：

```bash
uv add modelscope
uv run modelscope download --model BAAI/bge-large-zh-v1.5 --local_dir ./embeddingmodels/embedding
```

> 模型文件已加入 `.gitignore`，不会提交到仓库。

### 6️⃣ 启动后端

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 7️⃣ 启动前端

```bash
cd frontend
npm install
npm run dev
```

### 8️⃣ 访问系统

- 后端 API 文档：http://localhost:8000/docs
- 前端页面：http://localhost:3000

---

## 📂 项目结构

```
SugarGuardAI/
├── main.py                # FastAPI 应用入口（根目录）
├── app/                   # 后端应用
│   ├── config.py          # 配置（数据库、Tortoise ORM）
│   ├── database.py        # Tortoise ORM 注册
│   ├── models/            # 数据模型（patient/blood_sugar/diet_record/medication/exercise/health_report/chat_history）
│   ├── routers/           # 路由层（7 个业务模块）
│   ├── schemas/           # Pydantic 请求/响应模型
│   └── core/              # AI 核心
│       ├── llm_client.py       # 大模型客户端
│       ├── langgraph_agent.py  # LangGraph Agent 工作流
│       ├── rag_engine.py       # RAG 检索引擎
│       ├── vector_store.py     # ChromaDB 向量库
│       ├── knowledge_base.py   # 医学知识库
│       ├── health_analyzer.py  # 血糖数据分析
│       └── diet_advisor.py     # 饮食建议生成
├── frontend/              # 前端应用（Vue 3 + TS）
│   └── src/
│       ├── views/         # 页面（8 个功能页）
│       ├── api/           # API 封装
│       ├── stores/        # Pinia 状态管理
│       ├── components/    # 通用组件
│       ├── router/        # 路由
│       └── types/         # TS 类型定义
├── embeddingmodels/       # 本地 embedding 模型（gitignored）
├── data/                  # ChromaDB 持久化数据（gitignored）
├── .env                   # 环境变量（gitignored）
├── pyproject.toml         # uv 项目配置
└── README.md
```

---

## ⚙️ 环境变量说明

| 变量 | 说明 | 示例 |
| :--- | :--- | :--- |
| `DB_HOST` | 数据库地址 | `localhost` |
| `DB_PORT` | 数据库端口 | `3306` |
| `DB_USER` | 数据库用户 | `root` |
| `DB_PASSWORD` | 数据库密码 | `123456` |
| `DB_NAME` | 数据库名 | `diabetes` |
| `LLM_API_KEY` | 大模型 API Key | `sk-...` |
| `LLM_BASE_URL` | 大模型 Base URL（OpenAI 兼容） | `https://.../compatible-mode/v1` |
| `LLM_MODEL` | 模型名称 | `qwen3.8-flash` |
| `LLM_TEMPERATURE` | 采样温度 | `0.7` |
| `LLM_MAX_TOKENS` | 最大生成 token 数 | `1000` |
| `BG_LOW_THRESHOLD` | 低血糖阈值（mmol/L） | `3.9` |
| `BG_HIGH_THRESHOLD` | 高血糖阈值（mmol/L） | `10.0` |
| `CHROMA_PERSIST_DIR` | 向量库持久化目录 | `./data/chroma_db` |
| `CHROMA_COLLECTION_NAME` | 向量库集合名 | `medical_knowledge` |
| `RAG_TOP_K` | RAG 检索返回条数 | `5` |

---

## 🔒 安全说明

- 请勿将 `.env`、密钥、数据库凭证等敏感信息提交至仓库
- `.gitignore` 已默认排除敏感文件、缓存、本地模型与向量库数据
- 生产环境请使用环境变量或密钥管理服务注入凭证

---

## 📄 许可证

本项目仅供学习与个人使用，未经授权不得用于商业用途。

---

<div align="center">

**⭐ 如果本项目对您有帮助，欢迎 Star 支持！**

Made with ❤️ by [DingYH888](https://github.com/DingYH888)

</div>