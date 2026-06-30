from abc import ABC, abstractmethod

# 1. A Interface (Abstração da Estratégia)
class CategorizationStrategy(ABC):
    @abstractmethod
    def categorize(self, description: str) -> str:
        """Determina a categoria com base na descrição da transação."""
        pass

# 2. Estratégia Prática: Custo Fixo
class FixedCostStrategy(CategorizationStrategy):
    def categorize(self, description: str) -> str:
        palavras_chave = ["aluguel", "internet", "salario", "energia", "agua", "assinatura"]
        desc_lower = description.lower()
        if any(palavra in desc_lower for palavra in palavras_chave):
            return "fixo"
        return ""

# 3. Estratégia Prática: Custo Variável
class VariableCostStrategy(CategorizationStrategy):
    def categorize(self, description: str) -> str:
        palavras_chave = ["restaurante", "ifood", "uber", "combustivel", "mercado", "brinde"]
        desc_lower = description.lower()
        if any(palavra in desc_lower for palavra in palavras_chave):
            return "variável"
        return ""

# 4. O Contexto que a API vai utilizar
class CategorizationContext:
    def __init__(self):
        self._strategies = [FixedCostStrategy(), VariableCostStrategy()]

    def classificar(self, description: str) -> str:
        """Percorre as estratégias até achar uma regra válida. Se não achar, define como variável por padrão."""
        for strategy in self._strategies:
            resultado = strategy.categorize(description)
            if resultado:
                return resultado
        return "variável"