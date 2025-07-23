from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Account as AccountModel
from app.schemas import AccountCreate, AccountUpdate, AccountRead

router = APIRouter()

@router.post("/", response_model=AccountRead)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    db_account = AccountModel(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.get("/", response_model=list[AccountRead])
def list_accounts(db: Session = Depends(get_db)):
    return db.query(AccountModel).all()

@router.put("/{account_id}", response_model=AccountRead)
def update_account(account_id: int, update: AccountUpdate, db: Session = Depends(get_db)):
    db_account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    db_account.name = update.name
    db_account.starting_balance = update.starting_balance
    db.commit()
    db.refresh(db_account)
    return db_account

