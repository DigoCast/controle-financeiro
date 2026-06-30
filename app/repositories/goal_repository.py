from app.core.database import obter_conexao
from typing import List, Dict, Any

class GoalRepository:
    
    @staticmethod
    def salvar_meta(goal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Insere ou atualiza o teto de gastos para uma categoria."""
        query = """
            INSERT INTO budget_goals (category, max_limit)
            VALUES (%s, %s)
            ON CONFLICT (category) DO UPDATE 
            SET max_limit = EXCLUDED.max_limit
            RETURNING id;
        """
        with obter_conexao() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (goal_data["category"], goal_data["max_limit"]))
                goal_data["id"] = cur.fetchone()["id"]
                conn.commit()
                return goal_data

    @staticmethod
    def listar_metas() -> List[Dict[str, Any]]:
        """Busca os limites configurados."""
        query = "SELECT * FROM budget_goals;"
        with obter_conexao() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()