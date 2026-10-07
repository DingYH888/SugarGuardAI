<div align="center">

# 🩺 SugarGuardAI —— 智能慢性病管理系统

**基于 LLM 大模型 · Agent · RAG · LangGraph · LangChain 构建的 AI 智能健康管理平台**

为糖尿病患者提供 **7×24 小时** 个性化健康监测、饮食指导、用药管理、运动规划与 AI 健康咨询服务。

</div>

---

## 📖 项目简介

`SugarGuardAI` 是一款面向慢性病（以糖尿病为核心）人群的智能健康管理助手。系统融合大语言模型（LLM）、智能体（Agent）、检索增强生成（RAG）等前沿 AI 技术，结合患者实时健康数据与医学知识库，为每位用户量身定制：

- 🩸 **健康监测** —— 血糖、血压、体重等关键指标的趋势分析与异常预警
- 🥗 **饮食指导** —— 基于血糖反应与营养学的个性化食谱推荐
- 💊 **用药管理** —— 智能用药提醒、剂量核对与药物相互作用提示
- 🏃 **运动规划** —— 结合身体状况的科学运动方案与风险提示
- 🤖 **AI 健康咨询** —— 7×24 小时在线的智能健康问答助手

---

## 🛠️ 技术选型

| 分类 | 技术 / 工具 | 说明 |
| :--- | :--- | :--- |
| 开发操作系统 | ![Windows](https://img.shields.io/badge/Windows-11-0078D6?logo=windows&logoColor=white) | Windows 11 |
| 开发工具 | VSCode | 主开发环境 |
| Python 版本 | ![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | 3.12 |
| 项目管理工具 | uv | 高速 Python 包管理器 |
| 数据库 | MySQL 8 + Navicat | 关系型数据存储与可视化管理 |
| Web 框架 | FastAPI | 高性能异步 API 框架 |
| 服务器 | Uvicorn | ASGI 服务器 |
| ORM 框架 | Tortoise-ORM | 异步 ORM |
| AI 应用编排 | LangGraph | Agent 工作流编排 |
| 向量数据库 | ChromaDB | RAG 知识检索 |
| 大模型调用 | LangChain + OpenAI | LLM 接入与链式调用 |
| 前端框架 | Vue 3 + TypeScript | 响应式前端 + 类型安全 |

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

### 3️⃣ 后端启动

```bash
# 安装依赖
uv sync

# 配置环境变量
cp .env.example .env
# 编辑 .env，填写数据库连接、OpenAI API Key 等

# 启动服务
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4️⃣ 前端启动

```bash
cd frontend
npm install
npm run dev
```

### 5️⃣ 访问系统

- 后端 API 文档：http://localhost:8000/docs
- 前端页面：http://localhost:5173

---

## 📂 项目结构

```
SugarGuardAI/
├── app/                    # 后端应用（FastAPI）
│   ├── main.py             # 应用入口
│   ├── api/                # 路由层
│   ├── core/               # 核心配置
│   ├── models/             # 数据模型
│   ├── services/           # 业务服务
│   └── agents/             # LangGraph Agent 编排
├── frontend/               # 前端应用（Vue 3 + TS）
├── knowledge/              # RAG 知识库与文档
├── tests/                  # 测试用例
├── .env.example            # 环境变量示例
├── pyproject.toml          # uv 项目配置
└── README.md
```

---

## 🔒 安全说明

- 请勿将 `.env`、密钥、数据库凭证等敏感信息提交至仓库
- `.gitignore` 已默认排除敏感文件、缓存与环境配置
- 生产环境请使用环境变量或密钥管理服务注入凭证

---

## 📄 许可证

本项目仅供学习与个人使用，未经授权不得用于商业用途。

---

<div align="center">

**⭐ 如果本项目对您有帮助，欢迎 Star 支持！**

Made with ❤️ by [DingYH888](https://github.com/DingYH888)

</div>