# 🚀 云服务器部署指南

适用于：阿里云 / 腾讯云 / AWS / 其他 Linux 服务器

---

## 📋 前置要求

- 一台 Linux 服务器（Ubuntu 20.04+ 推荐）
- 服务器有公网 IP
- 可以 SSH 连接到服务器
- 域名（可选，用于 HTTPS）

---

## 🎯 快速部署（一键脚本）

### 步骤 1：SSH 连接到服务器

```bash
ssh root@your-server-ip
```

### 步骤 2：下载并运行部署脚本

```bash
# 下载脚本
wget https://raw.githubusercontent.com/ZhiXiaoCode/reward-task-platform/main/deploy-server.sh

# 给脚本执行权限
chmod +x deploy-server.sh

# 运行脚本
sudo ./deploy-server.sh
```

或者直接复制上面的脚本内容在服务器上执行。

---

## 🔧 手动部署步骤

如果自动脚本有问题，也可以手动部署：

### 1. 登录服务器并安装基础软件

```bash
ssh root@your-server-ip

# 更新系统
apt update && apt upgrade -y

# 安装必要软件
apt install -y git python3 python3-pip python3-venv nginx
```

### 2. 下载项目代码

```bash
cd /opt
git clone https://github.com/ZhiXiaoCode/reward-task-platform.git
cd reward-task-platform/backend
```

### 3. 设置 Python 环境

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 4. 初始化数据库

```bash
python init_db_local.py
```

### 5. 创建系统服务（systemd）

```bash
cat > /etc/systemd/system/reward-task.service << 'EOF'
[Unit]
Description=Reward Task Platform Backend
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/reward-task-platform/backend
Environment="PATH=/opt/reward-task-platform/backend/venv/bin"
ExecStart=/opt/reward-task-platform/backend/venv/bin/python run.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

### 6. 启动服务

```bash
systemctl daemon-reload
systemctl enable reward-task
systemctl start reward-task

# 查看状态
systemctl status reward-task
```

### 7. 配置 Nginx 反向代理

```bash
cat > /etc/nginx/sites-available/reward-task << 'EOF'
server {
    listen 80;
    server_name your-domain.com;  # 修改为您的域名或IP

    client_max_body_size 20M;

    location / {
        proxy_pass http://localhost:8011;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# 启用站点
ln -sf /etc/nginx/sites-available/reward-task /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 测试并重启 Nginx
nginx -t
systemctl restart nginx
```

---

## 🌐 配置 HTTPS（可选，推荐）

使用 Let's Encrypt 免费证书：

```bash
# 安装 Certbot
apt install -y certbot python3-certbot-nginx

# 获取证书（按照提示操作）
certbot --nginx -d your-domain.com

# 证书会自动续期
```

---

## 📊 常用管理命令

```bash
# 查看服务状态
systemctl status reward-task

# 查看日志
journalctl -u reward-task -f

# 重启服务
systemctl restart reward-task

# 停止服务
systemctl stop reward-task

# 查看 Nginx 状态
systemctl status nginx

# 查看 Nginx 访问日志
tail -f /var/log/nginx/access.log

# 查看 Nginx 错误日志
tail -f /var/log/nginx/error.log
```

---

## 🧪 验证部署

### 1. 检查服务是否运行

```bash
curl http://localhost:8011/health
```

应返回：
```json
{"status": "healthy", "timestamp": "..."}
```

### 2. 浏览器访问

- API 文档：`http://your-server-ip/docs`
- 健康检查：`http://your-server-ip/health`

---

## 📋 测试账号

| 角色 | 手机号 | 密码 | 余额 |
|------|--------|------|------|
| 用户 | 13800138000 | 123456 | ¥100 |
| 商家 | 13800138001 | 123456 | ¥1000 |

---

## ⚠️ 防火墙配置

如果无法访问，检查防火墙：

### Ubuntu (ufw)

```bash
ufw allow 80/tcp
ufw allow 443/tcp
ufw reload
```

### 阿里云/腾讯云安全组

在控制台的安全组规则中，开放：
- TCP 80 端口（HTTP）
- TCP 443 端口（HTTPS，可选）

---

## 📁 项目目录结构

```
/opt/reward-task-platform/
├── backend/
│   ├── venv/              # Python 虚拟环境
│   ├── app/               # 应用代码
│   ├── requirements.txt   # 依赖文件
│   └── run.py            # 启动脚本
└── frontend/             # 前端代码（需单独编译）
```

---

## 🔄 更新部署

```bash
cd /opt/reward-task-platform
git pull
systemctl restart reward-task
```

---

## 🆘 故障排查

### 服务无法启动

```bash
# 查看详细日志
journalctl -u reward-task -n 50 --no-pager
```

### 端口被占用

```bash
# 查看端口占用
netstat -tlnp | grep 8011
```

### Nginx 错误

```bash
# 测试配置
nginx -t

# 查看错误日志
tail -f /var/log/nginx/error.log
```

---

**部署完成后，记得告诉我您的服务器 IP！** 🎉

