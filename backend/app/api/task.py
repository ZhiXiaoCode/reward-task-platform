"""
API路由 - 任务模块
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
from datetime import datetime
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Task, TaskCategory, Transaction, TaskStatus
from app.schemas.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskSubmit,
    TaskVerify,
    TaskResponse,
    TaskListResponse,
    TaskCategoryResponse,
    ResponseModel
)

router = APIRouter(prefix="/tasks", tags=["任务"])


@router.get("/categories", response_model=ResponseModel)
async def get_categories(db: Session = Depends(get_db)):
    """获取任务分类"""
    categories = db.query(TaskCategory).filter(
        TaskCategory.is_active == True
    ).order_by(TaskCategory.sort_order).all()
    
    category_list = []
    for cat in categories:
        task_count = db.query(Task).filter(
            Task.category_id == cat.id,
            Task.status == TaskStatus.PENDING.value
        ).count()
        
        category_list.append({
            "id": cat.id,
            "name": cat.name,
            "icon": cat.icon,
            "description": cat.description,
            "sort_order": cat.sort_order,
            "task_count": task_count
        })
    
    return ResponseModel(code=1, msg="获取成功", data={"categories": category_list})


@router.get("", response_model=ResponseModel)
async def get_tasks(
    category_id: Optional[int] = None,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """获取任务列表"""
    query = db.query(Task)
    
    if category_id:
        query = query.filter(Task.category_id == category_id)
    
    if status:
        query = query.filter(Task.status == status)
    
    if keyword:
        query = query.filter(
            Task.title.contains(keyword) | Task.description.contains(keyword)
        )
    
    total = query.count()
    
    tasks = query.order_by(desc(Task.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size).all()
    
    task_list = []
    for task in tasks:
        publisher = db.query(User).filter(User.id == task.publisher_id).first()
        worker = db.query(User).filter(User.id == task.worker_id).first() if task.worker_id else None
        category = db.query(TaskCategory).filter(TaskCategory.id == task.category_id).first()
        
        task_list.append({
            "id": task.id,
            "title": task.title,
            "description": task.description[:100] + "..." if len(task.description) > 100 else task.description,
            "category_id": task.category_id,
            "category_name": category.name if category else "",
            "reward": task.reward,
            "status": task.status,
            "views": task.views,
            "participant_limit": task.participant_limit,
            "current_participants": task.current_participants,
            "publisher_id": task.publisher_id,
            "publisher_nickname": publisher.nickname if publisher else "",
            "worker_id": task.worker_id,
            "worker_nickname": worker.nickname if worker else "",
            "deadline": task.deadline.isoformat() if task.deadline else None,
            "created_at": task.created_at.isoformat()
        })
    
    return ResponseModel(
        code=1,
        msg="获取成功",
        data={
            "items": task_list,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    )


@router.get("/{task_id}", response_model=ResponseModel)
async def get_task_detail(
    task_id: int,
    db: Session = Depends(get_db)
):
    """获取任务详情"""
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task.views += 1
    db.commit()
    
    publisher = db.query(User).filter(User.id == task.publisher_id).first()
    worker = db.query(User).filter(User.id == task.worker_id).first() if task.worker_id else None
    category = db.query(TaskCategory).filter(TaskCategory.id == task.category_id).first()
    
    return ResponseModel(
        code=1,
        msg="获取成功",
        data={
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "requirements": task.requirements,
            "category_id": task.category_id,
            "category_name": category.name if category else "",
            "reward": task.reward,
            "status": task.status,
            "views": task.views,
            "participant_limit": task.participant_limit,
            "current_participants": task.current_participants,
            "publisher_id": task.publisher_id,
            "publisher_nickname": publisher.nickname if publisher else "",
            "worker_id": task.worker_id,
            "worker_nickname": worker.nickname if worker else "",
            "submit_content": task.submit_content,
            "submit_time": task.submit_time.isoformat() if task.submit_time else None,
            "verify_time": task.verify_time.isoformat() if task.verify_time else None,
            "verify_comment": task.verify_comment,
            "deadline": task.deadline.isoformat() if task.deadline else None,
            "created_at": task.created_at.isoformat()
        }
    )


@router.post("", response_model=ResponseModel)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建任务"""
    category = db.query(TaskCategory).filter(
        TaskCategory.id == task_data.category_id,
        TaskCategory.is_active == True
    ).first()
    
    if not category:
        raise HTTPException(status_code=400, detail="任务分类不存在")
    
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        requirements=task_data.requirements,
        category_id=task_data.category_id,
        reward=task_data.reward,
        participant_limit=task_data.participant_limit,
        deadline=task_data.deadline,
        publisher_id=current_user.id,
        status=TaskStatus.PENDING.value
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return ResponseModel(
        code=1,
        msg="任务创建成功",
        data={"task_id": new_task.id}
    )


@router.post("/{task_id}/accept", response_model=ResponseModel)
async def accept_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """接单任务"""
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    if task.status != TaskStatus.PENDING.value:
        raise HTTPException(status_code=400, detail="任务已不接受接单")
    
    if task.publisher_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能接自己的任务")
    
    if task.current_participants >= task.participant_limit:
        raise HTTPException(status_code=400, detail="任务参与人数已满")
    
    task.status = TaskStatus.IN_PROGRESS.value
    task.worker_id = current_user.id
    task.current_participants += 1
    
    if task.deadline is None:
        task.deadline = datetime.utcnow()
    
    db.commit()
    
    return ResponseModel(code=1, msg="接单成功")


@router.post("/{task_id}/submit", response_model=ResponseModel)
async def submit_task(
    task_id: int,
    submit_data: TaskSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """提交任务"""
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    if task.worker_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权提交此任务")
    
    if task.status != TaskStatus.IN_PROGRESS.value:
        raise HTTPException(status_code=400, detail="任务状态不允许提交")
    
    task.submit_content = submit_data.content
    task.submit_time = datetime.utcnow()
    task.status = TaskStatus.SUBMITTED.value
    
    db.commit()
    
    return ResponseModel(code=1, msg="提交成功，请等待审核")


@router.post("/{task_id}/verify", response_model=ResponseModel)
async def verify_task(
    task_id: int,
    verify_data: TaskVerify,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """审核任务（发布者审核）"""
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    if task.publisher_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权审核此任务")
    
    if task.status != TaskStatus.SUBMITTED.value:
        raise HTTPException(status_code=400, detail="任务状态不允许审核")
    
    task.verify_time = datetime.utcnow()
    task.verify_comment = verify_data.comment
    
    if verify_data.approved:
        task.status = TaskStatus.COMPLETED.value
        
        if task.worker:
            task.worker.balance += task.reward
            
            transaction = Transaction(
                user_id=task.worker_id,
                type="income",
                amount=task.reward,
                balance_after=task.worker.balance,
                description=f"完成任务：{task.title}",
                related_task_id=task.id
            )
            db.add(transaction)
        
        message = "审核通过，奖励已发放"
    else:
        task.status = TaskStatus.REJECTED.value
        message = "审核未通过，请重新提交"
    
    db.commit()
    
    return ResponseModel(code=1, msg=message)


@router.get("/my/published", response_model=ResponseModel)
async def get_my_published_tasks(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取我发布的任务"""
    query = db.query(Task).filter(Task.publisher_id == current_user.id)
    total = query.count()
    
    tasks = query.order_by(desc(Task.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size).all()
    
    task_list = []
    for task in tasks:
        category = db.query(TaskCategory).filter(TaskCategory.id == task.category_id).first()
        worker = db.query(User).filter(User.id == task.worker_id).first() if task.worker_id else None
        
        task_list.append({
            "id": task.id,
            "title": task.title,
            "description": task.description[:100] + "..." if len(task.description) > 100 else task.description,
            "category_name": category.name if category else "",
            "reward": task.reward,
            "status": task.status,
            "worker_nickname": worker.nickname if worker else "",
            "created_at": task.created_at.isoformat()
        })
    
    return ResponseModel(
        code=1,
        msg="获取成功",
        data={"items": task_list, "total": total, "page": page, "page_size": page_size}
    )


@router.get("/my/accepted", response_model=ResponseModel)
async def get_my_accepted_tasks(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取我接取的任务"""
    query = db.query(Task).filter(Task.worker_id == current_user.id)
    total = query.count()
    
    tasks = query.order_by(desc(Task.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size).all()
    
    task_list = []
    for task in tasks:
        category = db.query(TaskCategory).filter(TaskCategory.id == task.category_id).first()
        
        task_list.append({
            "id": task.id,
            "title": task.title,
            "description": task.description[:100] + "..." if len(task.description) > 100 else task.description,
            "category_name": category.name if category else "",
            "reward": task.reward,
            "status": task.status,
            "created_at": task.created_at.isoformat()
        })
    
    return ResponseModel(
        code=1,
        msg="获取成功",
        data={"items": task_list, "total": total, "page": page, "page_size": page_size}
    )
