"""
悬赏任务平台 - FastAPI主应用入口
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from app.core.config import settings
from app.core.database import engine, Base
from app.api import auth, user, task, account, notification, system

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="悬赏任务平台API",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """日志中间件"""
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    print(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    return JSONResponse(
        status_code=500,
        content={
            "code": 0,
            "msg": f"服务器内部错误: {str(exc)}",
            "data": None
        }
    )

app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(task.router, prefix="/api")
app.include_router(account.router, prefix="/api")
app.include_router(notification.router, prefix="/api")
app.include_router(system.router, prefix="/api")

@app.get("/")
async def root():
    """根路径"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
