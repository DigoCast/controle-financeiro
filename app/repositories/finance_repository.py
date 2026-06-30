from app.core.database import obter_conexao
from typing import List, Dict, Any

class TransactionRepository:
    
    @staticmethod
    def salvar(transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Insere uma nova transação com o valor criptografado no banco."""
        query = """
            INSERT INTO transactions (description, amount_encrypted, date, type, category)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """
        with obter_conexao() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    transaction_data["description"],
                    transaction_data["amount_encrypted"],
                    transaction_data["date"],
                    transaction_data["type"],
                    transaction_data["category"]
                ))
                novo_id = cur.fetchone()["id"]
                conn.commit()
                
                transaction_data["id"] = novo_id
                return transaction_data

    @staticmethod
    def listar_todas() -> List[Dict[str, Any]]:
        """Busca todas as transações cadastradas no banco."""
        query = "SELECT * FROM transactions;"
        with obter_conexao() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()