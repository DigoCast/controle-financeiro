from fastapi import FastAPI

app = FastAPI(
    title="Controle Financeiro API",
    description="MVP para o Laboratório de Engenharia de Software - Grupo 8",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "projeto": "Controle Financeiro",
        "grupo": "Grupo 8 - Diego & Davi"
    }