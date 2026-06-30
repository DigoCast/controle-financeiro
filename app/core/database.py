import psycopg
from psycopg.rows import dict_row
from app.core.config import settings

def obter_conexao():
    """Abre uma conexão usando a URL dinâmica do arquivo .env"""
    return psycopg.connect(settings.DATABASE_URL, row_factory=dict_row)

def inicializar_banco():
    """Cria as tabelas necessárias para o MVP se elas não existirem."""
    with obter_conexao() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id SERIAL PRIMARY KEY,
                    description TEXT NOT NULL,
                    amount_encrypted TEXT NOT NULL,
                    date DATE NOT NULL,
                    type TEXT NOT NULL,
                    category TEXT NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS budget_goals (
                    id SERIAL PRIMARY KEY,
                    category TEXT NOT NULL UNIQUE,
                    max_limit FLOAT NOT NULL
                );
            """)
            conn.commit()