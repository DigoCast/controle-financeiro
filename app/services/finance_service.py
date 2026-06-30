from app.repositories.finance_repository import TransactionRepository
from app.core.security import criptografar_valor, descriptografar_valor
from app.services.strategy import CategorizationContext
from typing import List, Dict, Any

class FinanceService:
    def __init__(self):
        self.contexto_categorizacao = CategorizationContext()

    def criar_transacao(self, transacao_schema) -> Dict[str, Any]:
        """Aplica as regras de negócio: categorização inteligente e criptografia."""
        dados = transacao_schema.model_dump()
        
        # Regra 1: Categorização Inteligente via Strategy Pattern se for uma despesa
        if dados["type"] == "despesa":
            dados["category"] = self.contexto_categorizacao.classificar(dados["description"])
        else:
            dados["category"] = "receita"

        # Regra 2: Criptografia contra vazamentos de dados sensíveis
        dados["amount_encrypted"] = criptografar_valor(dados["amount"])
        del dados["amount"]

        return TransactionRepository.salvar(dados)

    def listar_fluxo_caixa(self) -> List[Dict[str, Any]]:
        """Busca os dados brutos e descriptografa para exibição na API."""
        transacoes_criptografadas = TransactionRepository.listar_todas()
        
        fluxo_descriptografado = []
        for t in transacoes_criptografadas:
            t["amount"] = descriptografar_valor(t["amount_encrypted"])
            del t["amount_encrypted"]
            fluxo_descriptografado.append(t)
            
        return fluxo_descriptografado