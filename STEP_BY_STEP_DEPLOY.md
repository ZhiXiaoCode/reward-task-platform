# 🚀 详细部署步骤指南

## 概述

本指南将帮助您在 **5-10分钟内**完成部署，获得免费的体验域名！

---

## 第1部分：部署后端（Railway）

### 步骤1：访问 Railway

点击这个链接：https://railway.app/new

### 步骤2：选择部署方式

1. 点击 **"Deploy from GitHub repo"**
2. 点击 **"Configure GitHub App"**
3. 授权 Railway 访问您的 GitHub 账号
4. 选择 `reward-task-platform` 仓库

### 步骤3：开始部署

1. 点击 **"Deploy Now"**
2. 等待部署（约2-5分钟）
3. 您会看到构建日志滚动

### 步骤4：获取域名

部署成功后：
1. 点击项目设置（Settings）
2. 在 "Domains" 部分找到分配的域名
   - 例如：`https://reward-task-platform-xxxxx.up.railway.app`
3. **复制这个地址**，这就是您的后端 API 地址！

---

## 第2部分：配置前端

### 步骤1：修改 API 地址

打开文件：`frontend/config/api.config.js`

```javascript
// 修改为您的 Railway 域名
const BASE_URL = 'https://your-railway-domain.up.railway.app/api'
```

例如：
```javascript
const BASE_URL = 'https://reward-task-platform-12345.up.railway.app/api'
```

### 步骤2：提交修改

```bash
cd "/Users/a111/Documents/TRAE SOLO/reward-task-platform"
git add frontend/config/api.config.js
git commit -m "feat: 更新后端API地址"
git push
```

---

## 第3部分：部署前端（Vercel）

### 步骤1：访问 Vercel

点击这个链接：https://vercel.com/new

### 步骤2：导入仓库

1. 点击 **"Import"** 按钮
2. 选择 `reward-task-platform` 仓库
3. 点击 **"Import"**

### 步骤3：配置部署

1. **Root Directory**：选择 `frontend` 目录
2. **Framework Preset**：选择 `Other`
3. **Build Command**：留空
4. **Output Directory**：留空
5. 点击 **"Deploy"**

### 步骤4：获取前端域名

部署成功后，您会获得一个 H5 访问地址！

例如：`https://reward-task-platform.vercel.app`

---

## 第4部分：测试您的平台

### 测试后端

访问：`https://your-railway-domain.up.railway.app/docs`

您应该能看到 Swagger 文档！

### 测试前端

访问您的 Vercel 地址，尝试：

1. 注册新账号
2. 登录（测试账号：13800138000 / 123456）
3. 查看任务列表
4. 发布新任务
5. 接单任务

---

## 📱 恭喜！部署完成！

您现在拥有：

| 服务 | 地址 |
|------|------|
| **后端API** | https://your-domain.up.railway.app |
| **前端H5** | https://your-domain.vercel.app |
| **GitHub仓库** | https://github.com/ZhiXiaoCode/reward-task-platform |

---

## 💡 常见问题

### Q：部署失败怎么办？
A：查看构建日志，通常是依赖问题，重试即可。

### Q：前端无法访问后端？
A：检查 `api.config.js` 中的地址是否正确。

### Q：测试账号是什么？
A：
- 用户：13800138000 / 123456
- 商家：13800138001 / 123456

