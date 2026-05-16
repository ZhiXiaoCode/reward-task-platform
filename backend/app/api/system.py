"""
系统设置API
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User
from app.schemas.schemas import ResponseModel

router = APIRouter(prefix="/system", tags=["系统"])


@router.get("/config", response_model=ResponseModel)
async def get_system_config():
    """获取系统配置"""
    return ResponseModel(
        code=1,
        msg="获取成功",
        data={
            "app_name": "悬赏任务平台",
            "app_version": "3.0.0",
            "min_withdraw": 1.0,
            "withdraw_fee": 0,
            "customer_service": "400-888-8888",
            "about_us": "悬赏任务平台是一个安全可靠的悬赏任务交易平台..."
        }
    )


@router.get("/banners", response_model=ResponseModel)
async def get_banners():
    """获取首页轮播图"""
    banners = [
        {
            "id": 1,
            "image": "/static/banners/banner1.jpg",
            "link": "",
            "title": "新人福利"
        },
        {
            "id": 2,
            "image": "/static/banners/banner2.jpg",
            "link": "",
            "title": "任务升级"
        },
        {
            "id": 3,
            "image": "/static/banners/banner3.jpg",
            "link": "",
            "title": "邀请好友"
        }
    ]
    
    return ResponseModel(
        code=1,
        msg="获取成功",
        data={"banners": banners}
    )


@router.get("/announcements", response_model=ResponseModel)
async def get_announcements():
    """获取系统公告"""
    announcements = [
        {
            "id": 1,
            "title": "平台升级公告",
            "content": "平台已完成3.0版本升级...",
            "created_at": "2024-01-01 10:00:00"
        }
    ]
    
    return ResponseModel(
        code=1,
        msg="获取成功",
        data={"announcements": announcements}
    )


@router.post("/feedback", response_model=ResponseModel)
async def submit_feedback(
    content: str,
    contact: str = "",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """提交用户反馈"""
    # 实际应该存储到数据库
    print(f"收到用户反馈: {current_user.id} - {content}")
    
    return ResponseModel(code=1, msg="反馈已提交，感谢您的建议")
