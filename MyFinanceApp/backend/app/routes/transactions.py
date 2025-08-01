from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.db import get_db  # <-- Corrected import
from app.models import Transaction, Account

router = APIRouter(tags=["transactions"])  # Prefix handled in main.py

@router.post("/", response_model=schemas.TransactionRead)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    if transaction.type not in ["income", "expense", "transfer"]:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    if transaction.type in ["income", "expense"]:
        if not transaction.credit_card_used:
            if not transaction.account_id:
                raise HTTPException(status_code=400, detail="Account must be selected for income/expense transactions")
            account = db.query(models.Account).filter(models.Account.id == transaction.account_id).first()
            if not account:
                raise HTTPException(status_code=404, detail="Account not found")

            if transaction.type == "income":
                account.starting_balance += transaction.amount
            elif transaction.type == "expense":
                account.starting_balance -= transaction.amount

    elif transaction.type == "transfer":
        if not transaction.transfer_from_account_id or not transaction.transfer_to_account_id:
            raise HTTPException(status_code=400, detail="Both from and to accounts must be selected for transfers")

        from_account = db.query(models.Account).filter(models.Account.id == transaction.transfer_from_account_id).first()
        to_account = db.query(models.Account).filter(models.Account.id == transaction.transfer_to_account_id).first()

        if not from_account or not to_account:
            raise HTTPException(status_code=404, detail="Invalid from/to account for transfer")

        from_account.starting_balance -= transaction.amount
        to_account.starting_balance += transaction.amount

    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == db_transaction.id).first()
    return db_transaction

@router.get("/", response_model=list[schemas.TransactionRead])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(models.Transaction).order_by(models.Transaction.date.desc()).all()

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Reverse transaction effect
    if transaction.type in ["income", "expense"] and not transaction.credit_card_used:
        account = db.query(Account).filter(Account.id == transaction.account_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Associated account not found")

        if transaction.type == "income":
            account.starting_balance -= transaction.amount
        elif transaction.type == "expense":
            account.starting_balance += transaction.amount

    elif transaction.type == "transfer":
        from_account = db.query(Account).filter(Account.id == transaction.transfer_from_account_id).first()
        to_account = db.query(Account).filter(Account.id == transaction.transfer_to_account_id).first()

        if from_account:
            from_account.starting_balance += transaction.amount
        if to_account:
            to_account.starting_balance -= transaction.amount

    db.delete(transaction)
    db.commit()

    return {"message": "Transaction deleted and balances updated"}