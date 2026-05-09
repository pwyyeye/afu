# 阿福健康 - 前端应用

基于 Vue 3 + uni-app 的跨平台 AI 健康助手前端，支持 H5、微信小程序和原生 App。

## 技术栈

- **框架:** Vue 3 + uni-app (v3)
- **语言:** TypeScript
- **构建工具:** Vite 5
- **状态管理:** Pinia 2
- **HTTP 客户端:** luch-request 3
- **样式:** SCSS

## 项目结构

```
frontend/
├── src/
│   ├── main.ts              # 应用入口 (createSSRApp + Pinia)
│   ├── App.vue              # 根组件
│   ├── api/
│   │   └── request.ts       # HTTP 客户端封装 (JWT 注入、自动刷新)
│   ├── types/               # TypeScript 类型定义
│   │   ├── api.ts           # 通用响应类型
│   │   ├── user.ts          # 用户相关类型
│   │   ├── chat.ts          # 聊天相关类型
│   │   ├── health.ts        # 健康管理类型
│   │   └── report.ts        # 报告相关类型
│   ├── stores/              # Pinia 状态管理
│   │   ├── user.ts          # 认证状态 (登录、登出、Token)
│   │   ├── chat.ts          # 聊天会话、SSE 流式、图片/语音上传
│   │   ├── health.ts        # 健康档案、家庭、日记、目标、时间线
│   │   ├── report.ts        # 报告列表、详情、上传、对比
│   │   └── settings.ts      # 长辈模式、字号、通知、语音自动播放
│   ├── components/
│   │   ├── chat/            # 聊天组件 (气泡、输入框、语音录制)
│   │   ├── common/          # 通用组件 (空状态、弹窗、提示)
│   │   ├── report/          # 报告组件 (卡片、指标行、行动方案、红绿灯)
│   │   └── health/          # 健康组件
│   ├── pages/               # 页面 (18 个)
│   ├── styles/
│   │   └── common.scss      # 全局样式
│   └── utils/
│       ├── format.ts        # 格式化工具
│       └── storage.ts       # 存储工具
├── static/                  # 静态资源
│   ├── images/
│   └── tabbar/              # TabBar 图标 (5 个 Tab, 各 2 状态)
├── pages.json               # 页面路由与 TabBar 配置
├── manifest.json            # uni-app 应用配置
├── index.html               # HTML 入口
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 启动开发服务

```bash
# H5 (Web)
npm run dev:h5

# 微信小程序
npm run dev:mp-weixin

# 原生 App
npm run dev:app
```

### 3. 构建

```bash
npm run build:h5
npm run build:mp-weixin
npm run build:app
```

> H5 开发服务默认运行在 http://localhost:5173，后端 API 地址默认为 http://localhost:8002。

## 页面结构

### TabBar (5 个标签页)

| Tab | 页面 | 说明 |
|-----|------|------|
| 首页 | `pages/index/index` | 快捷操作、BMI 展示、健康小贴士、近期时间线 |
| 问答 | `pages/qa/index` | 聊天会话列表 |
| 报告 | `pages/report/index` | 体检报告列表 |
| 健康 | `pages/health/index` | 健康总览 |
| 我的 | `pages/profile/index` | 个人中心 |

### 完整页面列表 (18 个)

**登录**
- `pages/login/index` - 手机号 + 短信验证码登录

**问答**
- `pages/qa/index` - 聊天会话列表
- `pages/qa/chat` - 聊天页面 (SSE 流式响应、文本/语音/图片输入)

**报告**
- `pages/report/index` - 报告列表
- `pages/report/upload` - 上传报告
- `pages/report/detail` - 报告详情 (指标列表、红绿灯状态)
- `pages/report/compare` - 多报告趋势对比

**健康**
- `pages/health/index` - 健康概览
- `pages/health/profile` - 个人健康档案
- `pages/health/family` - 家庭成员列表
- `pages/health/member-edit` - 编辑家庭成员
- `pages/health/timeline` - 健康时间线
- `pages/health/diary` - 健康日记
- `pages/health/goals` - 健康目标

**我的**
- `pages/profile/index` - 个人中心
- `pages/profile/settings` - 设置
- `pages/profile/elder-mode` - 长辈模式配置

## 核心功能

### AI 健康问答

- 基于 Qwen LLM 的健康咨询对话
- SSE 流式响应，实时输出
- 支持发送图片 (药品、检查单拍照识别)
- 语音输入 (ASR 待实现)

### 体检报告分析

- 上传体检报告图片，AI 自动 OCR 识别
- 自动提取指标并标注红绿灯状态 (红/黄/蓝/绿)
- 生成整体健康评估和行动方案
- 多报告趋势对比，追踪指标变化

### 健康管理

- 个人健康档案 (血型、身高体重、过敏史、慢病、用药、手术史、家族史、生活习惯)
- 家庭成员管理，支持为家人建立独立档案
- 健康日记 (心情、标签、数值指标)
- 健康目标 (运动/饮食/习惯/体检，进度追踪)
- 统一时间线 (报告 + 日记合并展示)
- 提醒管理 (用药、体检、运动等)

### 长辈模式

- 大字体 (36rpx vs 标准 28rpx)
- 语音自动播放
- 简化界面

## 状态管理

| Store | 职责 |
|-------|------|
| `user` | 登录状态、Token 管理、用户信息 |
| `chat` | 会话列表、消息收发、SSE 流式连接 |
| `health` | 健康档案、家庭成员、日记、目标、时间线、提醒 |
| `report` | 报告列表、详情、上传、趋势对比 |
| `settings` | 长辈模式、字号、通知、语音播放设置 |

## HTTP 客户端

`src/api/request.ts` 基于 luch-request 封装：

- 自动注入 JWT Authorization Header
- Token 过期时自动使用 Refresh Token 刷新
- 刷新失败自动跳转登录页
- 统一错误处理

## 适配说明

- **H5:** 直接通过浏览器访问，开发时与后端 localhost:8002 通信
- **微信小程序:** 需在 `manifest.json` 中配置 AppID，上传代码需通过微信开发者工具
- **原生 App:** 通过 HBuilderX 或 CLI 打包
