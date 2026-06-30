from pydantic import BaseModel, Field
from datetime import date

class TransactionBase(BaseModel):
    description: str = Field(..., max_length=255)
    amount: float = Field(..., gt=0)
    date: date
    kind: str = Field(..., max_length=20) 

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    category: str = Field(..., max_length=50)

    class Config:
        from_attributes = True

class BudgetGoalBase(BaseModel):
    category: str = Field(..., max_length=50)
    max_limit: float = Field(..., gt=0)

class BudgetGoalCreate(BudgetGoalBase):
    pass

class BudgetGoal(BudgetGoalBase):
    id: int
    current_spent: float = 0.0

    class Config:
        from_attributes = True