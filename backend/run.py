"""
启动脚本
"""

import uvicorn
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("=" * 50)
    print("🏆 悬赏任务平台 - 后端服务")
    print("=" * 50)
    print("📚 API文档: http://localhost:8011/docs")
    print("📖 Redoc文档: http://localhost:8011/redoc")
    print("❤️  健康检查: http://localhost:8011/health")
    print("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8011,
        reload=True,
        log_level="info"
    )
