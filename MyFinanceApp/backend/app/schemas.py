from pydantic import BaseModel

class AccountCreate(BaseModel):
    name: str
    starting_balance: float

class AccountUpdate(BaseModel):
    name: str

class AccountRead(BaseModel):
    id: int
    name: str
    starting_balance: float

    class Config:
        orm_mode = True

