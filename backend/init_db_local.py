#!/usr/bin/env python3
"""
数据库初始化脚本 - 本地版
"""

import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal, Base
from app.models.models import TaskCategory, User, Task, TaskStatus
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import random


def init_database():
    """初始化数据库"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        print("=" * 50)
        print("🔧 开始初始化数据库...")
        print("=" * 50)
        
        # 检查是否已有分类数据
        existing_categories = db.query(TaskCategory).count()
        if existing_categories == 0:
            print("📦 初始化任务分类...")
            init_categories(db)
        else:
            print(f"✅ 任务分类已存在 ({existing_categories} 个)")
        
        # 检查是否已有测试用户
        existing_users = db.query(User).count()
        if existing_users == 0:
            print("👤 创建测试用户...")
            user1, user2 = init_test_users(db)
        else:
            print(f"✅ 测试用户已存在 ({existing_users} 个)")
            user1 = db.query(User).filter(User.phone == "13800138000").first()
            user2 = db.query(User).filter(User.phone == "13800138001").first()
        
        # 检查是否已有示例任务
        existing_tasks = db.query(Task).count()
        if existing_tasks == 0 and user1 and user2:
            print("📋 创建示例任务...")
            init_sample_tasks(db, user1, user2)
        else:
            print(f"✅ 示例任务已存在 ({existing_tasks} 个)")
        
        print("=" * 50)
        print("✅ 数据库初始化完成！")
        print("=" * 50)
        
        print("\n📋 测试账号信息:")
        print("-" * 50)
        print("用户账号: 13800138000")
        print("用户密码: 123456")
        print("账户余额: ¥100")
        print("-" * 50)
        print("商家账号: 13800138001")
        print("商家密码: 123456")
        print("账户余额: ¥1000")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


def init_categories(db: Session):
    """初始化任务分类"""
    categories = [
        {
            "name": "注册任务",
            "icon": "/static/icons/register.png",
            "description": "APP注册、账号申请等任务，完成简单注册即可获得奖励",
            "sort_order": 1
        },
        {
            "name": "下载任务",
            "icon": "/static/icons/download.png",
            "description": "应用下载、试用等任务，下载并体验应用即可获得奖励",
            "sort_order": 2
        },
        {
            "name": "关注任务",
            "icon": "/static/icons/follow.png",
            "description": "社交关注、粉丝增长等任务，关注指定账号即可获得奖励",
            "sort_order": 3
        },
        {
            "name": "投票任务",
            "icon": "/static/icons/vote.png",
            "description": "投票评选、活动参与等任务，为指定对象投票即可获得奖励",
            "sort_order": 4
        },
        {
            "name": "问卷任务",
            "icon": "/static/icons/survey.png",
            "description": "问卷调查、市场调研等任务，完成问卷调查即可获得奖励",
            "sort_order": 5
        },
        {
            "name": "其他任务",
            "icon": "/static/icons/other.png",
            "description": "其他类型的悬赏任务，各种新奇任务等你来发现",
            "sort_order": 6
        }
    ]
    
    for cat_data in categories:
        category = TaskCategory(**cat_data)
        db.add(category)
    
    db.commit()
    print(f"✅ 已创建 {len(categories)} 个任务分类")


def init_test_users(db: Session):
    """初始化测试用户"""
    user1 = User(
        phone="13800138000",
        password_hash=get_password_hash("123456"),
        nickname="测试用户小李",
        avatar="",
        balance=100.0
    )
    db.add(user1)
    
    user2 = User(
        phone="13800138001",
        password_hash=get_password_hash("123456"),
        nickname="商家老王",
        avatar="",
        balance=1000.0
    )
    db.add(user2)
    
    db.commit()
    print(f"✅ 已创建 2 个测试用户")
    return user1, user2


def init_sample_tasks(db: Session, user1: User, user2: User):
    """初始化示例任务"""
    categories = db.query(TaskCategory).all()
    
    sample_tasks = [
        {
            "title": "注册送现金活动",
            "description": "新用户注册即送现金奖励，简单几步完成注册即可获得10元现金奖励，名额有限，先到先得！",
            "requirements": "1. 从未注册过本平台\n2. 手机号需实名认证\n3. 注册后需完成新手任务",
            "category_id": categories[0].id,
            "reward": 10.0,
            "participant_limit": 1,
            "publisher_id": user2.id
        },
        {
            "title": "下载APP体验任务",
            "description": "下载指定APP并完成体验任务，体验金即可到账，操作简单，奖励丰厚！",
            "requirements": "1. 下载APP\n2. 注册账号\n3. 完成新手引导\n4. 体验5分钟",
            "category_id": categories[1].id,
            "reward": 5.0,
            "participant_limit": 5,
            "publisher_id": user2.id
        },
        {
            "title": "关注公众号得红包",
            "description": "关注指定公众号并互动，即可获得现金红包奖励，关注后截图提交即可！",
            "requirements": "1. 关注公众号\n2. 互动留言\n3. 截图提交",
            "category_id": categories[2].id,
            "reward": 3.0,
            "participant_limit": 10,
            "publisher_id": user2.id
        },
        {
            "title": "为喜欢的选手投票",
            "description": "为2024年度最佳员工投票，选出你心中的NO.1，投票即可获得奖励！",
            "requirements": "1. 进入投票页面\n2. 选择指定选手\n3. 提交投票截图",
            "category_id": categories[3].id,
            "reward": 2.0,
            "participant_limit": 20,
            "publisher_id": user2.id
        },
        {
            "title": "问卷调查奖励活动",
            "description": "完成简短的市场调研问卷，帮助我们改进产品，问卷完成后立即获得奖励！",
            "requirements": "1. 认真填写问卷\n2. 问卷需完整作答\n3. 回答需真实有效",
            "category_id": categories[4].id,
            "reward": 8.0,
            "participant_limit": 3,
            "publisher_id": user2.id
        },
        {
            "title": "新手试玩任务",
            "description": "试玩平台指定功能，了解平台操作流程，轻松完成即可获得奖励！",
            "requirements": "1. 了解平台功能\n2. 体验核心功能\n3. 提交体验报告",
            "category_id": categories[5].id,
            "reward": 6.0,
            "participant_limit": 5,
            "publisher_id": user2.id
        },
        {
            "title": "邀请好友注册",
            "description": "邀请好友注册平台，双方均可获得现金奖励，好友越多奖励越多！",
            "requirements": "1. 分享邀请链接\n2. 好友成功注册\n3. 好友完成首单",
            "category_id": categories[0].id,
            "reward": 15.0,
            "participant_limit": 10,
            "publisher_id": user2.id
        },
        {
            "title": "抖音点赞任务",
            "description": "为指定视频点赞并评论，简单的点赞操作即可获得奖励！",
            "requirements": "1. 点赞指定视频\n2. 评论指定内容\n3. 截图提交",
            "category_id": categories[2].id,
            "reward": 1.5,
            "participant_limit": 15,
            "publisher_id": user2.id
        }
    ]
    
    for i, task_data in enumerate(sample_tasks):
        deadline = datetime.utcnow() + timedelta(days=random.randint(7, 30))
        task = Task(
            title=task_data["title"],
            description=task_data["description"],
            requirements=task_data["requirements"],
            category_id=task_data["category_id"],
            reward=task_data["reward"],
            participant_limit=task_data["participant_limit"],
            publisher_id=task_data["publisher_id"],
            status=TaskStatus.PENDING.value,
            views=random.randint(10, 100),
            deadline=deadline
        )
        db.add(task)
    
    db.commit()
    print(f"✅ 已创建 {len(sample_tasks)} 个示例任务")


if __name__ == "__main__":
    init_database()

