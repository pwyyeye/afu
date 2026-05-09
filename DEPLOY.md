# 阿福健康 - 部署指南

## 架构

```
GitHub Pages (前端 H5)  ──HTTP──►  Railway (后端 API + SQLite)
pwyyeye.github.io/afu             *.up.railway.app
```

---

## 一、部署后端到 Railway

### 1. 注册并创建项目

1. 打开 [railway.app](https://railway.app)，用 GitHub 账号登录
2. 点击 **New Project** → **Deploy from GitHub Repo**
3. 选择 `pwyyeye/afu` 仓库
4. Railway 会自动识别根目录的 `railway.json`，但需要手动指定构建目录

### 2. 配置 Root Directory

进入项目 → 点击服务卡片 → **Settings** → **Source**：
- **Root Directory**: `backend`
- **Dockerfile Path**: `Dockerfile`（相对于 backend 目录）

### 3. 添加环境变量

进入 **Variables** 标签，添加以下变量：

| 变量 | 值 | 说明 |
|------|-----|------|
| `DATABASE_URL` | `sqlite:///./data/afu.db` | SQLite 数据库路径 |
| `JWT_SECRET_KEY` | 随机字符串 | 用于签发 JWT，务必修改 |
| `DASHSCOPE_API_KEY` | `sk-xxx` | 百炼 API Key |
| `CORS_ORIGINS` | `["https://pwyyeye.github.io"]` | 允许前端跨域访问 |

> `PORT` 变量由 Railway 自动注入，无需手动设置。

### 4. 获取后端域名

部署成功后：
1. 进入服务 → **Settings** → **Networking**
2. 点击 **Generate Domain**，获得类似 `afu-backend-production-xxxx.up.railway.app` 的域名
3. 记下这个域名，后面配置前端要用

### 5. 验证后端

```bash
curl https://afu-backend-production-xxxx.up.railway.app/health
# 应返回: {"status":"ok"}
```

---

## 二、部署前端到 GitHub Pages

### 1. 启用 GitHub Pages

进入仓库 **Settings** → **Pages** → **Source** 选择 **GitHub Actions**

### 2. 配置后端 API 地址

进入仓库 **Settings** → **Secrets and variables** → **Actions** → **Variables**，添加：

| Name | Value |
|------|-------|
| `VITE_API_BASE_URL` | 第一步拿到的后端域名，如 `https://afu-backend-production-xxxx.up.railway.app` |

### 3. 触发部署

在 GitHub Actions 页面点击 **Deploy** → **Run workflow**，或推送代码自动触发。

部署完成后访问: `https://pwyyeye.github.io/afu/`

---

## 三、本地开发

### 后端

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings openai python-multipart pypdf Pillow python-jose[cryptography] httpx
cp .env.example .env   # 编辑 .env 填入 DASHSCOPE_API_KEY
uvicorn app.main:app --reload --port 8002
```

### 前端

```bash
cd frontend
npm install
npm run dev:h5
```

本地开发默认连接 `http://localhost:8002`，无需额外配置。

---

## 四、常见问题

### 前端页面空白 / 资源 404

GitHub Pages 部署在子路径 `/afu/`。vite.config.ts 的 `base` 由 `VITE_BASE_PATH` 环境变量控制，workflow 中已设为 `/afu/`。如改仓库名，需同步修改。

### CORS 跨域报错

后端 `CORS_ORIGINS` 必须包含前端域名 `https://pwyyeye.github.io`。

### Railway 冷启动慢

免费 tier 闲置后会休眠，首次请求需 10-30 秒。可考虑升级或添加定时 ping。

### 后端报错 "disallowed host"

Railway 的代理会在 header 中设置 `Host` 为内部地址。如果 uvicorn 报 host 校验错误，启动命令加上 `--proxy-headers --forwarded-allow-ips='*'`。
