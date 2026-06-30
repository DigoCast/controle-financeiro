from fastapi import APIRouter, HTTPException, status
from app.models.finance import Transaction, TransactionCreate, BudgetGoal, BudgetGoalCreate
from app.services.finance_service import FinanceService
from typing import List

router = APIRouter(prefix="/finance", tags=["Controle Financeiro"])
servico_financas = FinanceService()

@router.post("/transactions", response_model=Transaction, status_code=status.HTTP_201_CREATED)
def cadastrar_transacao(transacao: TransactionCreate):
    """
    Rota para registrar uma nova transação.
    O sistema irá categorizá-la automaticamente via Strategy Pattern e criptografar o valor.
    """
    try:
        nova_transacao = servico_financas.criar_transacao(transacao)
        return nova_transacao
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar transação no banco: {str(e)}"
        )

@router.get("/transactions", response_model=List[Transaction])
def obter_fluxo_caixa():
    """
    Rota para listar todas as transações.
    Os valores sensíveis serão descriptografados em tempo real para a exibição do fluxo visual.
    """
    try:
        return servico_financas.listar_fluxo_caixa()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar fluxo de caixa: {str(e)}"
        )

@router.post("/goals", response_model=BudgetGoal, status_code=status.HTTP_201_CREATED)
def cadastrar_meta(meta: BudgetGoalCreate):
    """Define um limite de gastos máximo para uma categoria (fixo ou variável)."""
    try:
        return servico_financas.criar_meta(meta)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
def obter_resumo_financeiro():
    """Retorna o saldo, projeção e os alertas caso as metas tenham estourado."""
    try:
        return servico_financas.obter_resumo_e_alertas()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))