# 🔧 快速开始指南

## ⚡ 一键启动（推荐）

### macOS / Linux

```bash
cd "/Users/a111/Documents/TRAE SOLO/reward-task-platform"

# 赋予执行权限（仅首次需要）
chmod +x start.py

# 启动
python start.py
```

### Windows

```bash
cd "C:\Users\...\reward-task-platform"

# 启动
python start.py
```

---

## 📋 手动启动

### 1. 启动后端

```bash
cd "/Users/a111/Documents/TRAE SOLO/reward-task-platform/backend"

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python scripts/init_db.py

# 启动服务
python run.py
```

### 2. 访问服务

| 服务 | 地址 |
|------|------|
| **API文档** | http://localhost:8000/docs |
| **健康检查** | http://localhost:8000/health |
| **根路径** | http://localhost:8000/ |

### 3. 运行前端

使用 **HBuilderX**：
1. 打开 HBuilderX
2. 文件 → 导入 → 从本地目录导入
3. 选择 `frontend` 文件夹
4. 在项目上右键 → 运行 → 运行到浏览器

---

## 🧪 测试账号

初始化完成后自动创建：

| 角色 | 手机号 | 密码 | 余额 |
|------|--------|------|------|
| **用户** | 13800138000 | 123456 | ¥100 |
| **商家** | 13800138001 | 123456 | ¥1000 |

---

## 📱 测试流程

### 用户端流程
1. 打开App → 登录（13800138000 / 123456）
2. 首页查看任务列表
3. 点击任务 → 查看详情
4. 点击"立即接单"
5. 完成任务后 → 提交任务
6. 查看余额变化

### 商家端流程
1. 登录（13800138001 / 123456）
2. 点击"发布任务"
3. 填写任务信息（标题、奖励等）
4. 发布任务
5. 用户接单 → 提交
6. 进入"我发布的"审核
7. 审核通过 → 奖励发放

---

## 🔧 常见问题

### Q1: 启动报错 "Module not found"
```bash
# 重新安装依赖
pip install -r requirements.txt
```

### Q2: 端口被占用
```bash
# 修改 backend/app/core/config.py
# 找到 PORT 配置，改为其他端口（如 8001）
```

### Q3: 数据库错误
```bash
# 删除数据库文件，重新初始化
rm backend/reward_task.db
python scripts/init_db.py
```

### Q4: 前端无法连接后端
确保后端已启动，并检查：
```javascript
// frontend/config/api.config.js
const BASE_URL = 'http://localhost:8000/api'
```

---

## 🎯 功能验证清单

- [ ] 后端启动成功
- [ ] API文档可访问
- [ ] 前端页面加载
- [ ] 用户登录正常
- [ ] 商家登录正常
- [ ] 任务列表显示
- [ ] 任务发布成功
- [ ] 任务接单成功
- [ ] 任务提交成功
- [ ] 任务审核成功
- [ ] 余额变动正确
- [ ] 交易记录生成

---

## 📞 获取帮助

- 📖 API文档: http://localhost:8000/docs
- 📋 项目说明: README.md
- 🔍 部署清单: DEPLOYMENT_CHECKLIST.md

---

**祝您使用愉快！🎉**
