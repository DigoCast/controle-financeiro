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
        valor_original = dados["amount"]
        
        # Regra 1: Categorização Inteligente via Strategy Pattern
        if dados["kind"] == "despesa": 
            dados["category"] = self.contexto_categorizacao.classificar(dados["description"])
        else:
            dados["category"] = "receita"

        # Regra 2: Criptografia para persistência segura
        dados["amount_encrypted"] = criptografar_valor(dados["amount"])
        del dados["amount"]
        resultado_banco = TransactionRepository.salvar(dados)
        resultado_banco["amount"] = valor_original
        if "amount_encrypted" in resultado_banco:
            del resultado_banco["amount_encrypted"]
            
        return resultado_banco

    def listar_fluxo_caixa(self) -> List[Dict[str, Any]]:
        """Busca os dados brutos e descriptografa para exibição na API."""
        transacoes_criptografadas = TransactionRepository.listar_todas()
        
        fluxo_descriptografado = []
        for t in transacoes_criptografadas:
            t["amount"] = descriptografar_valor(t["amount_encrypted"])
            del t["amount_encrypted"]
            fluxo_descriptografado.append(t)
            
        return fluxo_descriptografado