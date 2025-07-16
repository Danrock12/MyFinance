# backend/app/main.py
from fastapi import FastAPI
from app.routes import transactions

app = FastAPI()
app.include_router(transactions.router, prefix="/transactions")

