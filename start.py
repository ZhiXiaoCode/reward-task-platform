"""
一键启动脚本
快速启动后端服务和初始化数据库
"""

import os
import sys
import subprocess
import time
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
DB_FILE = PROJECT_ROOT / "backend" / "reward_task.db"


def print_banner():
    """打印横幅"""
    print("=" * 60)
    print("🎯 悬赏任务平台 v3.0")
    print("=" * 60)
    print()


def check_python():
    """检查Python版本"""
    print("📌 检查Python环境...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python版本过低: {version.major}.{version.minor}")
        print("   请使用Python 3.8或更高版本")
        return False
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """检查并安装依赖"""
    print("\n📦 检查依赖...")
    requirements_file = BACKEND_DIR / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt 文件不存在")
        return False
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            check=True,
            capture_output=True
        )
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False


def init_database():
    """初始化数据库"""
    print("\n🗄️  初始化数据库...")
    
    if DB_FILE.exists():
        response = input("   数据库已存在，是否重新初始化？(y/N): ")
        if response.lower() != 'y':
            print("   跳过数据库初始化")
            return True
        DB_FILE.unlink()
        print("   已删除旧数据库")
    
    init_script = BACKEND_DIR / "scripts" / "init_db.py"
    
    if not init_script.exists():
        print("❌ 初始化脚本不存在")
        return False
    
    try:
        subprocess.run([sys.executable, str(init_script)], check=True)
        print("✅ 数据库初始化完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False


def start_server():
    """启动服务器"""
    print("\n🚀 启动服务器...")
    print("   后端地址: http://localhost:8011")
    print("   API文档:  http://localhost:8011/docs")
    print("   按 Ctrl+C 停止服务")
    print()
    
    try:
        run_script = BACKEND_DIR / "run.py"
        subprocess.run([sys.executable, str(run_script)], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 服务已停止")
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动失败: {e}")


def main():
    """主函数"""
    print_banner()
    
    if not check_python():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    if not init_database():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 准备就绪！")
    print("=" * 60)
    
    start_server()


if __name__ == "__main__":
    main()
