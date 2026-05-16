# 悬赏任务平台 - 后端

基于 FastAPI 构建的悬赏任务平台后端服务。

## 🚀 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python run.py
```

或者：

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 访问API文档

打开浏览器访问：http://localhost:8000/docs

## 📁 项目结构

```
backend/
├── app/
│   ├── api/           # API路由
│   │   ├── auth.py    # 认证
│   │   ├── user.py    # 用户
│   │   ├── task.py    # 任务
│   │   └── account.py # 账户
│   ├── core/          # 核心配置
│   │   ├── config.py  # 配置
│   │   ├── database.py # 数据库
│   │   └── security.py # 安全工具
│   ├── models/        # 数据库模型
│   ├── schemas/       # Pydantic模型
│   └── main.py        # 应用入口
├── requirements.txt
└── run.py
```

## 🔐 API接口

### 认证
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/refresh` - 刷新Token
- `POST /api/auth/logout` - 用户登出

### 用户
- `GET /api/user/profile` - 获取资料
- `PUT /api/user/profile` - 更新资料
- `POST /api/user/password` - 修改密码

### 任务
- `GET /api/tasks/categories` - 获取分类
- `GET /api/tasks` - 获取任务列表
- `GET /api/tasks/{id}` - 获取任务详情
- `POST /api/tasks` - 创建任务
- `POST /api/tasks/{id}/accept` - 接单任务
- `POST /api/tasks/{id}/submit` - 提交任务
- `POST /api/tasks/{id}/verify` - 审核任务

### 账户
- `GET /api/account/balance` - 获取余额
- `GET /api/account/transactions` - 交易记录
- `POST /api/account/withdraw` - 申请提现
- `GET /api/account/withdrawals` - 提现记录

## 🛠️ 技术栈

- **框架**: FastAPI
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **ORM**: SQLAlchemy
- **认证**: JWT
- **密码加密**: bcrypt
