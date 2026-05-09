# 阿福健康 (Afu Health)

AI 驱动的智能健康助手，提供健康问答、体检报告分析、个人健康管理等服务。

## 功能特性

- **AI 健康问答** — 基于 Qwen 大模型的健康咨询对话，支持 SSE 流式响应、图片识别、语音输入
- **体检报告分析** — 上传报告图片自动 OCR 识别，提取指标并标注红绿灯状态，生成健康评估和行动方案
- **报告趋势对比** — 多份报告跨年对比，追踪血糖、血脂等指标变化趋势
- **健康档案** — 血型、身高体重、过敏史、慢病、用药、手术史、家族史、生活习惯
- **家庭成员管理** — 为家人建立独立健康档案，聊天和报告可关联家庭成员
- **健康日记** — 每日健康记录，支持心情、标签、数值指标
- **健康目标** — 运动/饮食/习惯/体检目标设定与进度追踪
- **健康时间线** — 报告与日记合并的统一时间线
- **提醒管理** — 用药、体检、运动等定时提醒
- **长辈模式** — 大字体、语音自动播放、简化界面

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + uni-app + TypeScript + Pinia + Vite 5 |
| 后端 | FastAPI + SQLAlchemy 2.0 + Pydantic v2 |
| 数据库 | SQLite |
| AI 模型 | 阿里云百炼 DashScope (Qwen3.6-Plus / Qwen3-VL-Max) |
| 认证 | JWT (HS256, Access + Refresh Token) |

## 项目结构

```
afu/
├── frontend/                # 前端 (Vue 3 + uni-app)
│   ├── src/
│   │   ├── api/             # HTTP 客户端、LLM 直连服务
│   │   ├── stores/          # Pinia 状态管理 (chat, report, health, user, settings)
│   │   ├── pages/           # 页面 (18 个)
│   │   ├── components/      # 组件 (chat, report, common)
│   │   ├── types/           # TypeScript 类型定义
│   │   └── utils/           # 工具函数
│   ├── pages.json           # 路由与 TabBar 配置
│   └── manifest.json        # uni-app 应用配置
├── backend/                 # 后端 (FastAPI)
│   ├── app/
│   │   ├── api/v1/          # API 路由 (auth, chat, reports, health, users)
│   │   ├── models/          # 数据模型 (10 个表)
│   │   ├── schemas/         # Pydantic 请求/响应模型
│   │   ├── services/        # 业务逻辑 (LLM, 报告分析)
│   │   └── core/            # 安全、异常处理
│   ├── prompts/             # LLM 系统提示词
│   └── data/                # SQLite 数据库
├── .github/workflows/       # CI/CD 自动部署
├── docker-compose.yml       # Docker 本地运行
└── DEPLOY.md                # 部署指南
```

## 快速开始

### 环境要求

- Node.js 18+
- Python 3.10+

### 1. 克隆项目

```bash
git clone https://github.com/pwyyeye/afu.git
cd afu
```

### 2. 启动后端

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings openai python-multipart pypdf Pillow python-jose[cryptography] httpx

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入 DASHSCOPE_API_KEY

uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

API 文档: http://localhost:8002/docs

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev:h5
```

访问 http://localhost:5173

## 页面结构

| Tab | 页面 | 说明 |
|-----|------|------|
| 首页 | `pages/index` | 快捷操作、BMI、健康贴士、时间线 |
| 问答 | `pages/qa` | AI 健康咨询 (SSE 流式、图片、语音) |
| 报告 | `pages/report` | 体检报告管理、上传、趋势对比 |
| 健康 | `pages/health` | 档案、家庭、日记、目标、时间线 |
| 我的 | `pages/profile` | 个人中心、设置、长辈模式 |

## API 接口

所有业务接口前缀 `/api/v1`，详见 http://localhost:8002/docs

| 模块 | 主要接口 |
|------|---------|
| 认证 | `POST /auth/sms/login`, `POST /auth/refresh` |
| 问答 | `POST /chat/sessions/{id}/messages/stream` (SSE 流式) |
| 报告 | `POST /reports/upload` (图片 OCR + AI 分析) |
| 健康 | `/health/profile`, `/health/family`, `/health/diary`, `/health/goals`, `/health/reminders`, `/health/timeline` |

## 部署

详见 [DEPLOY.md](DEPLOY.md)

- **前端**: GitHub Pages (GitHub Actions 自动部署)
- **后端**: Railway / Render / Docker

## License

MIT
