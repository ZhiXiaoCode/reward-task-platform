"""
数据库模型定义
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class TaskStatus(str, enum.Enum):
    """任务状态枚举"""
    PENDING = "pending"        # 待接单
    IN_PROGRESS = "in_progress"  # 进行中
    SUBMITTED = "submitted"    # 已提交
    COMPLETED = "completed"    # 已完成
    REJECTED = "rejected"      # 已拒绝
    CANCELLED = "cancelled"    # 已取消


class TransactionType(str, enum.Enum):
    """交易类型枚举"""
    INCOME = "income"          # 收入
    EXPENSE = "expense"        # 支出
    WITHDRAW = "withdraw"      # 提现
    DEPOSIT = "deposit"        # 充值


class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nickname = Column(String(50), default="")
    avatar = Column(String(500), default="")
    balance = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    published_tasks = relationship("Task", back_populates="publisher", foreign_keys="Task.publisher_id")
    accepted_tasks = relationship("Task", back_populates="worker", foreign_keys="Task.worker_id")
    transactions = relationship("Transaction", back_populates="user")


class TaskCategory(Base):
    """任务分类模型"""
    __tablename__ = "task_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    icon = Column(String(255), default="")
    description = Column(Text, default="")
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    tasks = relationship("Task", back_populates="category")


class Task(Base):
    """任务模型"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text, default="")
    category_id = Column(Integer, ForeignKey("task_categories.id"), nullable=False)
    reward = Column(Float, nullable=False)  # 奖励金额
    status = Column(String(20), default=TaskStatus.PENDING.value)
    views = Column(Integer, default=0)  # 浏览量
    participant_limit = Column(Integer, default=1)  # 参与人数限制
    current_participants = Column(Integer, default=0)  # 当前参与人数
    
    publisher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    submit_content = Column(Text, default="")  # 提交内容
    submit_time = Column(DateTime, nullable=True)
    verify_time = Column(DateTime, nullable=True)
    verify_comment = Column(Text, default="")  # 审核备注
    
    deadline = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    category = relationship("TaskCategory", back_populates="tasks")
    publisher = relationship("User", back_populates="published_tasks", foreign_keys=[publisher_id])
    worker = relationship("User", back_populates="accepted_tasks", foreign_keys=[worker_id])


class Transaction(Base):
    """交易记录模型"""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(20), nullable=False)  # income, expense, withdraw, deposit
    amount = Column(Float, nullable=False)
    balance_after = Column(Float, nullable=False)  # 交易后余额
    description = Column(String(500), default="")
    related_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    status = Column(String(20), default="completed")  # pending, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    user = relationship("User", back_populates="transactions")


class WithdrawalRequest(Base):
    """提现申请模型"""
    __tablename__ = "withdrawal_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)  # wechat, alipay, bank
    account_info = Column(String(255), nullable=False)  # 账户信息（加密存储）
    status = Column(String(20), default="pending")  # pending, approved, rejected
    remark = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)


class SystemNotification(Base):
    """系统通知模型"""
    __tablename__ = "system_notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # NULL表示全体用户
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    type = Column(String(20), default="system")  # system, task, account
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
