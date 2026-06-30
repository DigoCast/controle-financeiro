from cryptography.fernet import Fernet

CHAVE_TEXTO = b'7_XdfG_TkXh8zR2-X8Q8Ym5C4U3V6_Z9M1k2P3q4w5e='
CHAVE_VALIDA = Fernet.generate_key() 

fernet = Fernet(CHAVE_VALIDA)

def criptografar_valor(valor: float) -> str:
    """Transforma um valor numérico (saldo/receita) em uma string criptografada."""
    texto_valor = str(valor)
    texto_criptografado = fernet.encrypt(texto_valor.encode())
    return texto_criptografado.decode()

def descriptografar_valor(texto_criptografado: str) -> float:
    """Recupera o valor numérico original a partir da string criptografada."""
    try:
        texto_descriptografado = fernet.decrypt(texto_criptografado.encode()).decode()
        return float(texto_descriptografado)
    except Exception:
        return 0.0