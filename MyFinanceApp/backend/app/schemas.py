from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional, Literal

class AccountBase(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class TransactionBase(BaseModel):
    date: date
    name: str
    tag: str
    amount: float
    type: Literal['income', 'expense', 'transfer']
    account_id: Optional[int] = None
    transfer_from_account_id: Optional[int] = None
    transfer_to_account_id: Optional[int] = None
    credit_card_used: bool = False
    credit_card_name: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: int

    # Add nested account info here:
    account: Optional[AccountBase] = None
    transfer_from_account: Optional[AccountBase] = None
    transfer_to_account: Optional[AccountBase] = None

    model_config = ConfigDict(from_attributes=True)

class AccountCreate(BaseModel):
    name: str
    starting_balance: float

class AccountUpdate(AccountCreate):
    pass

class AccountRead(AccountCreate):
    id: int
    balance: float

    model_config = ConfigDict(from_attributes=True)

