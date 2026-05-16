"""
API路由 - 用户模块
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, get_current_user
from app.models.models import User
from app.schemas.schemas import (
    UserProfile,
    UserUpdate,
    ChangePassword,
    ResponseModel
)

router = APIRouter(prefix="/user", tags=["用户"])


@router.get("/profile", response_model=ResponseModel)
async def get_profile(current_user: User = Depends(get_current_user)):
    """获取用户资料"""
    return ResponseModel(
        code=1,
        msg="获取成功",
        data={
            "id": current_user.id,
            "phone": current_user.phone,
            "nickname": current_user.nickname,
            "avatar": current_user.avatar,
            "balance": current_user.balance,
            "is_active": current_user.is_active,
            "created_at": current_user.created_at.isoformat()
        }
    )


@router.put("/profile", response_model=ResponseModel)
async def update_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户资料"""
    if user_data.nickname is not None:
        current_user.nickname = user_data.nickname
    if user_data.avatar is not None:
        current_user.avatar = user_data.avatar
    
    db.commit()
    db.refresh(current_user)
    
    return ResponseModel(
        code=1,
        msg="更新成功",
        data={
            "id": current_user.id,
            "phone": current_user.phone,
            "nickname": current_user.nickname,
            "avatar": current_user.avatar
        }
    )


@router.post("/password", response_model=ResponseModel)
async def change_password(
    password_data: ChangePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改密码"""
    if not verify_password(password_data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="原密码错误"
        )
    
    current_user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    
    return ResponseModel(code=1, msg="密码修改成功")
