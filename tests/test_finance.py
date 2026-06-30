from app.services.strategy import CategorizationContext

def test_deve_categorizar_custo_como_fixo():
    """Valida se o Strategy Pattern reconhece custos fixos automaticamente."""
    contexto = CategorizationContext()
    
    # Testando palavras-chave mapeadas na estratégia de custo fixo
    resultado_aluguel = contexto.classificar("Aluguel da sede da PME")
    resultado_internet = contexto.classificar("Conta de Internet mensal")
    
    assert resultado_aluguel == "fixo"
    assert resultado_internet == "fixo"

def test_deve_categorizar_custo_como_variavel_por_padrao():
    """Valida se o sistema joga para variável caso não combine com nenhuma regra fixa."""
    contexto = CategorizationContext()
    
    # Testando algo que deve cair no fallback de custo variável
    resultado_ifood = contexto.classificar("ifood com a gata")
    resultado_aleatorio = contexto.classificar("compra de canetas azuis")
    
    assert resultado_ifood == "variável"
    assert resultado_aleatorio == "variável"