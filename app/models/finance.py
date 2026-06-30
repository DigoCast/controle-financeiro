from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

# 1. Modelo para Transações (Entradas e Saídas)
class TransactionBase(BaseModel):
    description: str = Field(..., example="Aluguel do Escritório")
    amount: float = Field(..., gt=0, example=1500.00)
    date: date = Field(..., example="2026-07-01")
    type: str = Field(..., example="despesa") # "receita" ou "despesa"

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    category: str = Field(..., example="fixo") # "fixo", "variável" ou "receita"

    class Config:
        from_attributes = True


# 2. Modelo para as Metas de Orçamento
class BudgetGoalBase(BaseModel):
    category: str = Field(..., example="variável") # Alvo do alerta
    max_limit: float = Field(..., gt=0, example=500.00)

class BudgetGoalCreate(BudgetGoalBase):
    pass

class BudgetGoal(BudgetGoalBase):
    id: int
    current_spent: float = 0.0

    class Config:
        from_attributes = True