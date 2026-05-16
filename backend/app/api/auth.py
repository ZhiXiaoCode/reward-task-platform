"""
API路由 - 认证模块
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token,
    get_current_user
)
from app.core.config import settings
from app.models.models import User
from app.schemas.schemas import (
    UserRegister,
    UserLogin,
    Token,
    UserProfile,
    ChangePassword,
    ResponseModel
)

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=ResponseModel)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """用户注册"""
    existing_user = db.query(User).filter(User.phone == user_data.phone).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该手机号已注册"
        )
    
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        phone=user_data.phone,
        password_hash=hashed_password,
        nickname=user_data.nickname or f"用户{user_data.phone[-4:]}"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": new_user.id})
    refresh_token = create_refresh_token(data={"sub": new_user.id})
    
    return ResponseModel(
        code=1,
        msg="注册成功",
        data={
            "user": {
                "id": new_user.id,
                "phone": new_user.phone,
                "nickname": new_user.nickname,
                "avatar": new_user.avatar,
                "balance": new_user.balance
            },
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    )


@router.post("/login", response_model=ResponseModel)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    user = db.query(User).filter(User.phone == user_data.phone).first()
    
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="手机号或密码错误"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用"
        )
    
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return ResponseModel(
        code=1,
        msg="登录成功",
        data={
            "user": {
                "id": user.id,
                "phone": user.phone,
                "nickname": user.nickname,
                "avatar": user.avatar,
                "balance": user.balance
            },
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    )


@router.post("/refresh", response_model=ResponseModel)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """刷新Token"""
    payload = verify_token(refresh_token, "refresh")
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌"
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已被禁用"
        )
    
    new_access_token = create_access_token(data={"sub": user.id})
    new_refresh_token = create_refresh_token(data={"sub": user.id})
    
    return ResponseModel(
        code=1,
        msg="刷新成功",
        data={
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }
    )


@router.post("/logout", response_model=ResponseModel)
async def logout(current_user: User = Depends(get_current_user)):
    """用户登出"""
    return ResponseModel(code=1, msg="登出成功")
