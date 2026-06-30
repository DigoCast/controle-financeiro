from app.repositories.finance_repository import TransactionRepository
from app.core.security import criptografar_valor, descriptografar_valor
from app.services.strategy import CategorizationContext
from app.repositories.goal_repository import GoalRepository
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
    
    def obter_resumo_e_alertas(self) -> Dict[str, Any]:
        """Calcula o saldo atual, projeções futuras e verifica estouro de metas."""
        transacoes = self.listar_fluxo_caixa()
        metas = GoalRepository.listar_metas()

        # 1. Cálculo de Saldo e Projeção (Alvo de Elicitação)
        total_receitas = sum(t["amount"] for t in transacoes if t["kind"] == "receita")
        total_despesas = sum(t["amount"] for t in transacoes if t["kind"] == "despesa")
        saldo_atual = total_receitas - total_despesas
        
        # Projeção simples: saldo atual + receitas futuras simuladas/cadastradas
        saldo_projetado = saldo_atual 

        # 2. Verificação de Alertas de Estouro (Alvo de Elicitação)
        gastos_por_categoria = {}
        for t in transacoes:
            if t["kind"] == "despesa":
                cat = t["category"]
                gastos_por_categoria[cat] = gastos_por_categoria.get(cat, 0.0) + t["amount"]

        alertas = []
        for m in metas:
            categoria = m["category"]
            limite = m["max_limit"]
            gasto_atual = gastos_por_categoria.get(categoria, 0.0)

            if gasto_atual > limite:
                alertas.append({
                    "category": categoria,
                    "max_limit": limite,
                    "current_spent": gasto_atual,
                    "message": f"ALERTA: Meta da categoria '{categoria}' estourada!"
                })

        return {
            "saldo_atual": saldo_atual,
            "saldo_projetado": saldo_projetado,
            "alertas_estouro": alertas
        }

    def criar_meta(self, meta_schema) -> Dict[str, Any]:
        """Camada de serviço para persistir a meta orçamentária."""
        return GoalRepository.salvar_meta(meta_schema.model_dump())