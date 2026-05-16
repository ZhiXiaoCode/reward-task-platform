# 部署指南

## 📦 项目已上传到 GitHub

**GitHub 仓库地址**: https://github.com/ZhiXiaoCode/reward-task-platform

---

## 🚀 快速部署方案

### 方案1：Railway（推荐，一键部署）

**优点**：免费，一键部署，自动域名

**部署步骤**：
1. 访问 https://railway.app/new
2. 点击 "Deploy from GitHub repo"
3. 授权访问 `reward-task-platform`
4. 选择仓库，点击 "Deploy Now"
5. 等待部署完成（约2-5分钟）
6. 获取分配的域名（例如：`xxx.railway.app`）

---

### 方案2：Vercel（前端）+ Railway（后端）

**前端（Vercel）**：
1. 访问 https://vercel.com/new
2. 导入仓库，选择 `frontend` 目录
3. 部署，获得域名

**后端（Railway）**：同方案1

---

### 方案3：Render（免费托管）

**后端部署**：
1. 访问 https://render.com
2. 点击 "New Web Service"
3. 连接 GitHub 仓库
4. 配置：
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run.py`
5. 部署

---

## 📱 前端部署配置

修改 `frontend/config/api.config.js`:
```javascript
// 替换为您的后端域名
const BASE_URL = 'https://your-api-domain.com/api'
```

---

## 🎯 推荐部署流程

### 第1步：部署后端（Railway）
1. 打开 https://railway.app
2. 点击 "New Project" → "Deploy from GitHub repo"
3. 选择 `reward-task-platform`
4. 选择根目录（默认）
5. 点击 "Deploy Now"

### 第2步：获取后端域名
部署成功后，在 Railway 项目设置中找到分配的域名，例如：
```
https://reward-task-platform.up.railway.app
```

### 第3步：更新前端配置
修改 `frontend/config/api.config.js`:
```javascript
const BASE_URL = 'https://reward-task-platform.up.railway.app/api'
```

### 第4步：部署前端（Vercel）
1. 打开 https://vercel.com/new
2. 导入仓库
3. 选择 `frontend` 目录
4. 部署，获得 H5 访问地址

---

## 🔧 环境变量配置

### Railway 环境变量
在 Railway 项目设置中添加：
```env
SECRET_KEY=your-random-secret-key-here
DEBUG=False
```

---

## 📋 部署后验证

### 后端验证
1. 访问 `https://your-domain.com/docs`
2. 查看 Swagger 文档
3. 测试健康检查 `https://your-domain.com/health`

### 前端验证
1. 打开前端地址
2. 尝试注册/登录
3. 查看任务列表
4. 测试任务发布

---

## 🎉 完成！

部署成功后，您将获得：
- ✅ 后端 API 域名
- ✅ 前端 H5 访问地址
- ✅ 完整的悬赏任务平台

---

## 💡 其他部署选项

| 平台 | 免费额度 | 支持 |
|------|---------|------|
| **Railway** | $5/月 | ✅ 推荐 |
| **Render** | 免费额度 | ✅ 简单 |
| **Fly.io** | 免费额度 | ✅ 可扩展 |
| **Vercel** | 免费无限 | ✅ 前端专用 |

