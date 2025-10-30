from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import extract
from typing import Dict, Any
from app.db import get_db
from app.models import Account, Transaction

router = APIRouter()

@router.get("/{year}")
def get_financial_report(year: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    try:
        accounts = db.query(Account).all()

        report = []
        totals_start = 0.0
        totals_monthly = [0.0] * 12

        for account in accounts:
            # Get all transactions for this account and year
            transactions = (
                db.query(Transaction)
                .filter(Transaction.account_id == account.id)
                .filter(extract("year", Transaction.date) == year)
                .all()
            )

            # Sum transactions by month
            monthly_sums = [0.0] * 12
            for t in transactions:
                month_index = t.date.month - 1
                amt = t.amount if t.type == "income" else -t.amount
                monthly_sums[month_index] += amt

            # Build cumulative monthly balances
            cumulative = []
            running_total = account.starting_balance
            for m in range(12):
                running_total += monthly_sums[m]
                cumulative.append(round(running_total, 2))
                totals_monthly[m] += running_total

            totals_start += account.starting_balance

            report.append({
                "account_name": account.name,
                "start": round(account.starting_balance, 2),
                "monthly": cumulative
            })

        return {
            "year": year,
            "report": report,
            "totals": {
                "start": round(totals_start, 2),
                "monthly": [round(x, 2) for x in totals_monthly],
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
