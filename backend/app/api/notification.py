"""
消息通知API
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, SystemNotification
from app.schemas.schemas import ResponseModel

router = APIRouter(prefix="/notifications", tags=["通知"])


@router.get("", response_model=ResponseModel)
async def get_notifications(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取通知列表"""
    query = db.query(SystemNotification).filter(
        (SystemNotification.user_id == current_user.id) | 
        (SystemNotification.user_id == None)
    )
    
    total = query.count()
    
    notifications = query.order_by(desc(SystemNotification.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size).all()
    
    notification_list = []
    for notif in notifications:
        notification_list.append({
            "id": notif.id,
            "title": notif.title,
            "content": notif.content,
            "type": notif.type,
            "is_read": notif.is_read,
            "created_at": notif.created_at.isoformat()
        })
    
    return ResponseModel(
        code=1,
        msg="获取成功",
        data={
            "items": notification_list,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    )


@router.get("/unread-count", response_model=ResponseModel)
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取未读通知数量"""
    count = db.query(SystemNotification).filter(
        SystemNotification.is_read == False,
        (SystemNotification.user_id == current_user.id) | 
        (SystemNotification.user_id == None)
    ).count()
    
    return ResponseModel(
        code=1,
        msg="获取成功",
        data={"count": count}
    )


@router.post("/{notification_id}/read", response_model=ResponseModel)
async def mark_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """标记通知为已读"""
    notification = db.query(SystemNotification).filter(
        SystemNotification.id == notification_id,
        (SystemNotification.user_id == current_user.id) | 
        (SystemNotification.user_id == None)
    ).first()
    
    if not notification:
        return ResponseModel(code=0, msg="通知不存在")
    
    notification.is_read = True
    db.commit()
    
    return ResponseModel(code=1, msg="标记成功")


@router.post("/read-all", response_model=ResponseModel)
async def mark_all_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """标记所有通知为已读"""
    db.query(SystemNotification).filter(
        SystemNotification.is_read == False,
        (SystemNotification.user_id == current_user.id) | 
        (SystemNotification.user_id == None)
    ).update({"is_read": True})
    
    db.commit()
    
    return ResponseModel(code=1, msg="全部标记成功")
