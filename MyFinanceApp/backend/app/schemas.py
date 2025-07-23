from pydantic import BaseModel, ConfigDict

class AccountBase(BaseModel):
    name: str
    starting_balance: float

class AccountCreate(AccountBase):
    pass

class AccountUpdate(AccountBase):
    pass

class AccountRead(AccountBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

