#!/bin/bash

# ========================================
# 悬赏任务平台 - 云服务器自动部署脚本
# 适用于：阿里云 / 腾讯云 / 其他 Linux 服务器
# ========================================

echo "========================================"
echo "🏆 悬赏任务平台 - 部署脚本"
echo "========================================"

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  请使用 root 用户运行此脚本"
    echo "使用命令：sudo $0"
    exit 1
fi

# 更新系统
echo "📦 更新系统..."
apt update && apt upgrade -y

# 安装必要软件
echo "📦 安装必要软件..."
apt install -y git python3 python3-pip python3-venv nginx

# 创建项目目录
PROJECT_DIR="/opt/reward-task-platform"
echo "📂 创建项目目录：$PROJECT_DIR"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# 克隆或拉取代码
if [ -d ".git" ]; then
    echo "🔄 更新代码..."
    git pull
else
    echo "📥 克隆代码..."
    git clone https://github.com/ZhiXiaoCode/reward-task-platform.git .
fi

# 进入后端目录
cd backend

# 创建虚拟环境
echo "🐍 创建 Python 虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 安装依赖
echo "📦 安装 Python 依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 初始化数据库
echo "🗄️  初始化数据库..."
python init_db_local.py

# 创建 systemd 服务
echo "🔧 创建系统服务..."
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

# 重载并启动服务
echo "🚀 启动服务..."
systemctl daemon-reload
systemctl enable reward-task
systemctl start reward-task

# 配置 Nginx（可选）
echo "🌐 配置 Nginx..."
cat > /etc/nginx/sites-available/reward-task << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8011;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOF

# 启用站点
ln -sf /etc/nginx/sites-available/reward-task /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 测试并重启 Nginx
nginx -t && systemctl restart nginx

# 获取服务器 IP
SERVER_IP=$(curl -s ifconfig.me)

echo ""
echo "========================================"
echo "✅ 部署完成！"
echo "========================================"
echo ""
echo "🌐 访问地址："
echo "   后端 API：http://$SERVER_IP"
echo "   API 文档：http://$SERVER_IP/docs"
echo ""
echo "🔧 常用命令："
echo "   查看状态：systemctl status reward-task"
echo "   查看日志：journalctl -u reward-task -f"
echo "   重启服务：systemctl restart reward-task"
echo ""
echo "📋 测试账号："
echo "   用户：13800138000 / 123456"
echo "   商家：13800138001 / 123456"
echo ""

