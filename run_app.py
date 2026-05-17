import uvicorn
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    print("=" * 50)
    print("🏆 悬赏任务平台 - 后端服务")
    print("=" * 50)
    print(f"📚 API文档: http://localhost:{port}/docs")
    print(f"📖 Redoc文档: http://localhost:{port}/redoc")
    print(f"❤️  健康检查: http://localhost:{port}/health")
    print("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
