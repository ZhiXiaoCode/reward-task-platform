"""
Pydantic schemas - 数据验证模型
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ==================== 认证相关 ====================

class UserRegister(BaseModel):
    """用户注册"""
    phone: str = Field(..., min_length=11, max_length=11)
    password: str = Field(..., min_length=6, max_length=20)
    nickname: Optional[str] = ""
    
    @validator('phone')
    def validate_phone(cls, v):
        if not v.isdigit():
            raise ValueError('手机号必须是数字')
        if not v.startswith('1'):
            raise ValueError('手机号必须以1开头')
        return v


class UserLogin(BaseModel):
    """用户登录"""
    phone: str
    password: str


class Token(BaseModel):
    """Token响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token数据"""
    user_id: Optional[int] = None


# ==================== 用户相关 ====================

class UserBase(BaseModel):
    """用户基础信息"""
    phone: str
    nickname: str = ""
    avatar: str = ""


class UserCreate(UserBase):
    """用户创建"""
    password: str


class UserUpdate(BaseModel):
    """用户更新"""
    nickname: Optional[str] = None
    avatar: Optional[str] = None


class UserProfile(UserBase):
    """用户资料"""
    id: int
    balance: float
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChangePassword(BaseModel):
    """修改密码"""
    old_password: str
    new_password: str = Field(..., min_length=6, max_length=20)


# ==================== 任务相关 ====================

class TaskCategoryBase(BaseModel):
    """任务分类基础"""
    name: str
    icon: str = ""
    description: str = ""


class TaskCategoryCreate(TaskCategoryBase):
    """任务分类创建"""
    pass


class TaskCategoryResponse(TaskCategoryBase):
    """任务分类响应"""
    id: int
    sort_order: int
    task_count: Optional[int] = 0
    
    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    """创建任务"""
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    requirements: Optional[str] = ""
    category_id: int
    reward: float = Field(..., gt=0)
    participant_limit: int = Field(default=1, ge=1, le=10)
    deadline: Optional[datetime] = None


class TaskUpdate(BaseModel):
    """更新任务"""
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    reward: Optional[float] = None
    participant_limit: Optional[int] = None
    deadline: Optional[datetime] = None


class TaskSubmit(BaseModel):
    """提交任务"""
    content: str = Field(..., min_length=10)


class TaskVerify(BaseModel):
    """审核任务"""
    approved: bool
    comment: Optional[str] = ""


class TaskResponse(BaseModel):
    """任务响应"""
    id: int
    title: str
    description: str
    requirements: str = ""
    category_id: int
    category_name: Optional[str] = ""
    reward: float
    status: str
    views: int
    participant_limit: int
    current_participants: int
    publisher_id: int
    publisher_nickname: Optional[str] = ""
    worker_id: Optional[int] = None
    worker_nickname: Optional[str] = ""
    submit_content: Optional[str] = ""
    submit_time: Optional[datetime] = None
    verify_time: Optional[datetime] = None
    verify_comment: Optional[str] = ""
    deadline: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """任务列表响应"""
    items: List[TaskResponse]
    total: int
    page: int
    page_size: int


# ==================== 账户相关 ====================

class TransactionResponse(BaseModel):
    """交易记录响应"""
    id: int
    type: str
    amount: float
    balance_after: float
    description: str
    related_task_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class WithdrawalRequestCreate(BaseModel):
    """创建提现申请"""
    amount: float = Field(..., gt=0)
    payment_method: str  # wechat, alipay, bank
    account_info: str


class WithdrawalRequestResponse(BaseModel):
    """提现申请响应"""
    id: int
    amount: float
    payment_method: str
    status: str
    remark: str
    created_at: datetime
    processed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================== 通知相关 ====================

class NotificationResponse(BaseModel):
    """通知响应"""
    id: int
    title: str
    content: str
    type: str
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== 通用响应 ====================

class ResponseModel(BaseModel):
    """通用响应模型"""
    code: int = 1
    msg: str = "操作成功"
    data: Optional[dict] = None


class PageResponse(BaseModel):
    """分页响应"""
    items: List
    total: int
    page: int
    page_size: int
