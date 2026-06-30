from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from app.core.database import inicializar_banco
from app.controllers.finance_controller import router as finance_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        inicializar_banco()
        print("Banco de dados PostgreSQL inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar no PostgreSQL: {e}")
    
    yield 

app = FastAPI(
    title="Controle Financeiro API",
    description="MVP para o Laboratório de Engenharia de Software - Grupo 8",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(finance_router)

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "projeto": "Controle Financeiro",
        "grupo": "Grupo 8 - Diego & Davi"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)