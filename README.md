# 悬赏任务平台 v3.0

🎯 基于 FastAPI + UniApp 的悬赏任务平台

## 📱 项目简介

这是一个**全新的悬赏任务平台**，完全基于自建API开发，不依赖任何第三方服务。

### ✨ 核心特性

- 🔐 **安全认证** - JWT Token + bcrypt 密码加密
- 📱 **跨平台** - UniApp 支持 iOS、Android、H5
- ⚡ **高性能** - FastAPI 异步框架
- 🛡️ **数据安全** - Token 本地加密存储

## 🚀 快速开始

### 后端启动

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python scripts/init_db.py

# 启动服务
python run.py
```

### 前端运行

使用 HBuilderX 打开 `frontend` 目录，运行到浏览器/模拟器/真机。

## 🧪 测试账号

| 角色 | 手机号 | 密码 | 余额 |
|------|--------|------|------|
| 用户 | 13800138000 | 123456 | ¥100 |
| 商家 | 13800138001 | 123456 | ¥1000 |

## 📁 项目结构

```
reward-task-platform/
├── backend/          # FastAPI 后端
├── frontend/        # UniApp 前端
├── README.md
├── QUICK_START.md
└── DEPLOYMENT_CHECKLIST.md
```

## 📄 许可证

MIT License
