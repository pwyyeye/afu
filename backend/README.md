# 阿福健康 - 后端服务

基于 FastAPI 的 AI 健康助手后端 API，提供健康问答、体检报告分析、个人健康管理等服务。

## 技术栈

- **框架:** FastAPI
- **语言:** Python 3.10+
- **ORM:** SQLAlchemy 2.0
- **数据库:** SQLite
- **认证:** JWT (python-jose, HS256)
- **LLM:** 阿里云 DashScope (Qwen 系列模型)
- **文件处理:** pypdf (PDF), Pillow (图片)

## 项目结构

```
backend/
├── app/
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置管理 (pydantic-settings)
│   ├── dependencies.py      # FastAPI 依赖注入 (鉴权)
│   ├── api/v1/
│   │   ├── router.py        # 路由汇总 (/api/v1)
│   │   ├── auth.py          # 认证接口 (短信登录、Token 刷新)
│   │   ├── users.py         # 用户信息接口
│   │   ├── chat.py          # 健康问答接口 (SSE 流式、图片、语音)
│   │   ├── reports.py       # 体检报告接口 (上传、分析、对比)
│   │   └── health.py        # 健康管理接口 (档案、家庭、日记、目标、提醒、时间线)
│   ├── core/
│   │   ├── exceptions.py    # 自定义异常
│   │   └── security.py      # JWT 生成与验证
│   ├── database/
│   │   └── session.py       # 数据库引擎与会话
│   ├── models/              # SQLAlchemy 数据模型 (10 个)
│   ├── schemas/             # Pydantic 请求/响应模型
│   └── services/
│       ├── llm_service.py   # LLM 服务 (DashScope/Qwen, Mock 模式)
│       └── report_service.py # 报告分析流水线
├── prompts/                 # LLM 系统提示词
├── data/                    # SQLite 数据库文件
├── tests/                   # 测试目录
├── pyproject.toml           # 项目元数据与依赖
├── .env.example             # 环境变量模板
└── .env                     # 环境变量 (不提交到 Git)
```

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -e .
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，按需修改：

```bash
cp .env.example .env
```

关键配置项：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DATABASE_URL` | 数据库连接串 | `sqlite:///data/afu.db` |
| `JWT_SECRET_KEY` | JWT 签名密钥 | 需自行生成 |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Access Token 有效期 (分钟) | `15` |
| `JWT_REFRESH_TOKEN_EXPIRE_MINUTES` | Refresh Token 有效期 (分钟) | `10080` (7天) |
| `DASHSCOPE_API_KEY` | 阿里云 DashScope API Key | 空 (未配置时使用 Mock 模式) |
| `CORS_ORIGINS` | 允许的跨域来源 | `http://localhost:5173,http://localhost:3000` |

### 3. 启动服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

服务启动后访问:
- API 文档: http://localhost:8002/docs
- 健康检查: http://localhost:8002/health

## API 接口

所有业务接口前缀为 `/api/v1`。

### 认证 `/api/v1/auth/`

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/auth/sms/send` | 发送短信验证码 |
| POST | `/auth/sms/login` | 短信验证码登录 |
| POST | `/auth/refresh` | 刷新 Access Token |

> 开发模式下，验证码固定为 `123456`，且会在控制台打印。

### 用户 `/api/v1/users/`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/users/me` | 获取当前用户信息 |
| PUT | `/users/me` | 更新用户信息 |

### 健康问答 `/api/v1/chat/`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/chat/sessions` | 获取会话列表 |
| POST | `/chat/sessions` | 创建会话 |
| DELETE | `/chat/sessions/{id}` | 删除会话 |
| GET | `/chat/sessions/{id}/messages` | 获取会话消息 |
| POST | `/chat/sessions/{id}/messages` | 发送消息 (普通) |
| POST | `/chat/sessions/{id}/messages/stream` | 发送消息 (SSE 流式) |
| POST | `/chat/sessions/{id}/image` | 上传图片并分析 |
| POST | `/chat/sessions/{id}/voice` | 上传语音 (占位，ASR 未实现) |

### 体检报告 `/api/v1/reports/`

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/reports/upload` | 上传报告图片 (OCR + AI 分析) |
| GET | `/reports/` | 获取报告列表 |
| GET | `/reports/{id}` | 获取报告详情 (含指标) |
| GET | `/reports/compare` | 多报告趋势对比 |

### 健康管理 `/api/v1/health/`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET/PUT | `/health/profile` | 健康档案 CRUD |
| GET/POST/DELETE | `/health/family` | 家庭成员管理 |
| GET/POST | `/health/diary` | 健康日记 (分页) |
| GET/POST/PUT/DELETE | `/health/goals` | 健康目标管理 |
| GET/POST/PUT/DELETE | `/health/reminders` | 提醒管理 |
| GET | `/health/timeline` | 统一时间线 (报告 + 日记) |

## 数据模型

共 10 个数据表，均使用 UUID 主键和 `created_at` / `updated_at` 时间戳：

- **User** - 用户 (手机号、昵称、长辈模式、设置)
- **ChatSession** - 聊天会话
- **ChatMessage** - 聊天消息 (文本/图片/语音)
- **MedicalReport** - 体检报告 (红绿灯状态、摘要、行动方案)
- **ReportIndicator** - 报告指标 (名称、值、参考范围、趋势)
- **HealthProfile** - 健康档案 (血型、身高体重、过敏史、慢病、用药)
- **FamilyMember** - 家庭成员
- **HealthDiary** - 健康日记 (心情、标签、指标)
- **HealthGoal** - 健康目标 (运动/饮食/习惯/体检)
- **Reminder** - 提醒

## LLM 集成

- **文本模型:** `qwen-plus` - 用于健康问答和报告分析
- **视觉模型:** `qwen-vl-max` - 用于图片 OCR 和图像理解
- **Mock 模式:** 未配置 `DASHSCOPE_API_KEY` 时自动启用，返回预设的健康建议响应，便于本地开发
