# 阿福健康 - 部署指南

## 架构

```
GitHub Pages (前端)  ──►  Railway/Render (后端 API)
https://pwyyeye.github.io/afu    https://afu-api.xxx.com
```

## 一、前端部署到 GitHub Pages

### 1. 启用 GitHub Pages

1. 进入仓库 Settings → Pages
2. Source 选择 **GitHub Actions**

### 2. 配置后端 API 地址

进入仓库 Settings → Secrets and variables → Actions → Variables，添加：

| Name | Value |
|------|-------|
| `VITE_API_BASE_URL` | 你的后端 API 地址，如 `https://afu-backend.up.railway.app` |

### 3. 推送代码触发部署

```bash
git add .
git commit -m "feat: add deployment config"
git push origin main
```

Actions 会自动构建 H5 并部署到 `https://pwyyeye.github.io/afu/`

---

## 二、后端部署

### 方案 A: Railway (推荐，免费额度)

1. 访问 [railway.app](https://railway.app) 并用 GitHub 登录
2. New Project → Deploy from GitHub repo → 选择 `afu` 仓库
3. 设置 Root Directory 为 `backend`
4. 添加环境变量：

| 变量 | 值 |
|------|-----|
| `DATABASE_URL` | `sqlite:///./data/afu.db` |
| `JWT_SECRET_KEY` | 随机生成的密钥 |
| `DASHSCOPE_API_KEY` | 你的百炼 API Key |
| `CORS_ORIGINS` | `["https://pwyyeye.github.io"]` |

5. Railway 会自动检测 Dockerfile 并部署
6. 生成的域名类似 `afu-backend.up.railway.app`

### 方案 B: Render (免费额度)

1. 访问 [render.com](https://render.com) 并用 GitHub 登录
2. New → Web Service → 选择 `afu` 仓库
3. 设置：
   - Root Directory: `backend`
   - Environment: Docker
   - 同上添加环境变量
4. 部署完成后获得域名

### 方案 C: 本地 Docker 运行

```bash
# 确保 backend/.env 已配置
docker-compose up -d
```

后端运行在 `http://localhost:8002`

---

## 三、部署后验证

1. 打开 `https://pwyyeye.github.io/afu/`
2. 登录页面应正常显示
3. 发送健康问答，确认 AI 流式响应正常
4. 上传体检报告，确认分析功能正常

---

## 四、常见问题

### 前端 404

GitHub Pages 部署在子路径 `/afu/` 下，vite.config.ts 已配置 `base`。如果页面空白，检查浏览器控制台的资源加载路径。

### CORS 错误

后端 `CORS_ORIGINS` 必须包含前端域名 `https://pwyyeye.github.io`。

### 后端冷启动慢

Railway/Render 免费 tier 会在闲置后休眠，首次请求可能需要 10-30 秒。
