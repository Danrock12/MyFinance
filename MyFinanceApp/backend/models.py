# backend/app/models.py
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    name = Column(String(255))
    tag = Column(String(50))
    amount = Column(Float)
    type = Column(String(10))  # 'income' or 'expense'
    account = Column(String(255))

