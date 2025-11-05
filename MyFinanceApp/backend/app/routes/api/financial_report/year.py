from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Account, Transaction
from collections import defaultdict

router = APIRouter()

@router.get("/{year}")
async def get_report(year: int, db: Session = Depends(get_db)):
    # Get all accounts
    accounts = db.query(Account).all()
    if not accounts:
        raise HTTPException(status_code=404, detail="No accounts found")

    # Get transactions only for the requested year
    transactions = db.query(Transaction).filter(
        Transaction.date != None,
        Transaction.date.between(f"{year}-01-01", f"{year}-12-31")
    ).all()

    # Prepare data structures
    monthly_data = defaultdict(lambda: [0.0] * 12)
    starting_balances = {account.id: account.starting_balance for account in accounts}

    # Process each transaction
    for txn in transactions:
        month_idx = txn.date.month - 1
        if txn.type == "income":
            monthly_data[txn.account_id][month_idx] += txn.amount
        elif txn.type == "expense":
            monthly_data[txn.account_id][month_idx] -= txn.amount
        elif txn.type == "transfer":
            # Subtract from source account
            if txn.transfer_from_account_id:
                monthly_data[txn.transfer_from_account_id][month_idx] -= txn.amount
            # Add to destination account
            if txn.transfer_to_account_id:
                monthly_data[txn.transfer_to_account_id][month_idx] += txn.amount

    # Debug: print transaction dates and month indices
    for txn in transactions:
        print(f"Transaction {txn.id}: {txn.date} (month_idx={txn.date.month - 1})")

    # Build cumulative balances per account
    report = []
    for account in accounts:
        start = starting_balances.get(account.id, 0.0)
        running_total = start
        monthly_balances = []
        for i in range(12):
            running_total += monthly_data[account.id][i]
            monthly_balances.append(round(running_total, 2))
        report.append({
            "account_name": account.name,
            "monthly_balances": monthly_balances
        })

    # Compute totals for each month across all accounts
    totals = {
        "monthly": [
            round(sum(acc["monthly_balances"][i] for acc in report), 2)
            for i in range(12)
        ]
    }

    return {
        "year": year,
        "report": report,
        "totals": totals
    }