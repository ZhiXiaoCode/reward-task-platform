"""
API路由 - 账户模块
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Transaction, WithdrawalRequest
from app.schemas.schemas import ResponseModel

router = APIRouter(prefix="/account", tags=["账户"])


@router.get("/balance", response_model=ResponseModel)
async def get_balance(current_user: User = Depends(get_current_user)):
    """获取账户余额"""
    return ResponseModel(
        code=1,
        msg="获取成功",
        data={
            "balance": current_user.balance,
            "total_income": current_user.balance + 100.0,
            "total_withdraw": 0.0
        }
    )


@router.get("/transactions", response_model=ResponseModel)
async def get_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    transaction_type: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取交易记录"""
    query = db.query(Transaction).filter(Transaction.user_id == current_user.id)
    
    if transaction_type:
        query = query.filter(Transaction.type == transaction_type)
    
    total = query.count()
    
    transactions = query.order_by(desc(Transaction.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size).all()
    
    transaction_list = []
    for trans in transactions:
        transaction_list.append({
            "id": trans.id,
            "type": trans.type,
            "amount": trans.amount,
            "balance_after": trans.balance_after,
            "description": trans.description,
            "related_task_id": trans.related_task_id,
            "created_at": trans.created_at.isoformat()
        })
    
    return ResponseModel(
        code=1,
        msg="获取成功",
        data={
            "items": transaction_list,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    )


@router.post("/withdraw", response_model=ResponseModel)
async def create_withdrawal(
    amount: float,
    payment_method: str,
    account_info: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """申请提现"""
    if amount <= 0:
        raise HTTPException(status_code=400, detail="提现金额必须大于0")
    
    if amount > current_user.balance:
        raise HTTPException(status_code=400, detail="余额不足")
    
    if amount < 1:
        raise HTTPException(status_code=400, detail="最低提现金额为1元")
    
    if payment_method not in ["wechat", "alipay", "bank"]:
        raise HTTPException(status_code=400, detail="不支持的提现方式")
    
    current_user.balance -= amount
    
    withdrawal = WithdrawalRequest(
        user_id=current_user.id,
        amount=amount,
        payment_method=payment_method,
        account_info=account_info,
        status="pending"
    )
    db.add(withdrawal)
    
    transaction = Transaction(
        user_id=current_user.id,
        type="withdraw",
        amount=-amount,
        balance_after=current_user.balance,
        description=f"申请提现到{payment_method}"
    )
    db.add(transaction)
    
    db.commit()
    
    return ResponseModel(
        code=1,
        msg="提现申请已提交",
        data={"withdrawal_id": withdrawal.id}
    )


@router.get("/withdrawals", response_model=ResponseModel)
async def get_withdrawals(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取提现记录"""
    query = db.query(WithdrawalRequest).filter(
        WithdrawalRequest.user_id == current_user.id
    )
    total = query.count()
    
    withdrawals = query.order_by(desc(WithdrawalRequest.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size).all()
    
    withdrawal_list = []
    for wd in withdrawals:
        withdrawal_list.append({
            "id": wd.id,
            "amount": wd.amount,
            "payment_method": wd.payment_method,
            "status": wd.status,
            "remark": wd.remark,
            "created_at": wd.created_at.isoformat(),
            "processed_at": wd.processed_at.isoformat() if wd.processed_at else None
        })
    
    return ResponseModel(
        code=1,
        msg="获取成功",
        data={
            "items": withdrawal_list,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    )
