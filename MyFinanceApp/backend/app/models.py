from sqlalchemy import Column, Integer, String, Date, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    name = Column(String(255))
    tag = Column(String(50))
    amount = Column(Float)
    type = Column(String(10))  # 'income', 'expense', or 'transfer'
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=True)
    transfer_from_account_id = Column(Integer, ForeignKey('accounts.id'), nullable=True)
    transfer_to_account_id = Column(Integer, ForeignKey('accounts.id'), nullable=True)
    credit_card_used = Column(Boolean, default=False)
    credit_card_name = Column(String(255), nullable=True)

    account = relationship(
        "Account",
        foreign_keys=[account_id],
        back_populates="transactions"
    )
    transfer_from_account = relationship(
        "Account",
        foreign_keys=[transfer_from_account_id],
        back_populates="transfers_out"
    )
    transfer_to_account = relationship(
        "Account",
        foreign_keys=[transfer_to_account_id],
        back_populates="transfers_in"
    )


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    starting_balance = Column(Float, nullable=False)

    transactions = relationship(
        "Transaction",
        back_populates="account",
        foreign_keys="[Transaction.account_id]"
    )
    transfers_out = relationship(
        "Transaction",
        back_populates="transfer_from_account",
        foreign_keys="[Transaction.transfer_from_account_id]"
    )
    transfers_in = relationship(
        "Transaction",
        back_populates="transfer_to_account",
        foreign_keys="[Transaction.transfer_to_account_id]"
    )

    @property
    def balance(self) -> float:
        total = self.starting_balance
        for transaction in self.transactions:
            if transaction.type == 'income':
                total += transaction.amount
            elif transaction.type == 'expense':
                total -= transaction.amount
        for t in self.transfers_in:
            total += t.amount
        for t in self.transfers_out:
            total -= t.amount
        return total

