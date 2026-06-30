# Sistema de Controle Financeiro 💸
### Laboratório de Engenharia de Software | Grupo 8
**Integrantes:** Diego Castilho & Davi Miyake 

---

## 📌 Sobre o Projeto
Este projeto consiste em um MVP de um **Sistema de Controle Financeiro** desenvolvido em Python com FastAPI. O objetivo central do negócio é auxiliar pessoas físicas e PMEs a saírem do vermelho por meio de um acompanhamento visual de fluxo de caixa limpo e inteligência aplicada na gestão de despesas.

### Alvos de Elicitação Atendidos:
* **Categorização Inteligente de Custos:** Classificação automatizada de despesas entre custos fixos e variáveis.
* **Projeções de Saldo:** Cálculos baseados no fluxo consolidado de receitas futuras e despesas.
* **Alertas de Estouro:** Sistema de gatilhos automáticos que avisa quando os gastos de uma categoria ultrapassam as metas orçadas.
* **Segurança e Criptografia:** Blindagem dos dados de saldos e receitas contra vazamentos.

---

## 🏗️ Arquitetura do Sistema
O sistema foi construído seguindo rigorosamente o padrão de **Arquitetura em Camadas** para garantir o isolamento de responsabilidades e a manutenibilidade do código:

```text
    controle_financeiro/
    ├── app/
    │   ├── controllers/      # Camada de Apresentação (Rotas HTTP / FastAPI)
    │   ├── services/         # Camada de Negócio (Regras, Cálculos e Padrões)
    │   ├── repositories/     # Camada de Persistência (Interface direta com o PostgreSQL)
    │   ├── models/           # Camada de Domínio (Schemas e Validações do Pydantic)
    │   └── core/             # Camada Central (Configurações de ambiente e Segurança)
    ├── tests/                # Testes automatizados (Pytest)
    ├── main.py               # Ponto de entrada da aplicação
    └── .env                  # Variáveis de ambiente protegidas
```

---

## 🎨 Design Patterns Aplicados
Para atender aos requisitos técnicos de extensibilidade do laboratório, foi implementado o padrão Strategy (Estratégia) na camada de serviços.  
O CategorizationContext utiliza uma interface comum para avaliar dinamicamente as strings de descrição das transações. Se a descrição contiver gatilhos como "aluguel" ou "internet", a classe FixedCostStrategy assume a classificação. Caso contenha termos como "ifood" ou "uber", a VariableCostStrategy é acionada, eliminando a necessidade de condicionais `if/else` complexas no núcleo da aplicação.

## 🛡️ Mecanismos de Segurança (Proteção contra Vazamentos)
Para cumprir o requisito de blindagem de dados financeiros sensíveis, o sistema utiliza a biblioteca cryptography com criptografia simétrica baseada no algoritmo Fernet.  
* O valor numérico (amount) enviado pelo usuário é criptografado imediatamente na camada de negócio.
* O banco de dados PostgreSQL armazena apenas a string criptografada em um campo amount_encrypted.
* O valor só é descriptografado em memória no momento em que o usuário autenticado solicita a leitura dos dados.

---

## ⚙️ Como Configurar e Rodar o Projeto Localmente

### Pré-requisitos:
* `Python 3.13` instalado
* `PostgreSQL` instalado e rodando localmente

### 1. Clonar o repositório e criar o Ambiente Virtual  
No terminal `(Git Bash)`, execute:

```bash
    python -m venv .venv
    source .venv/Scripts/activate
```

### 2. Instalar as dependências
```bash
    pip install -r requirements.txt
```

### 3. Configurar as Variáveis de Ambiente
Crie um arquivo chamado `.env` na raiz do projeto e preencha com as suas credenciais locais do banco:

```bash
    cp .env.template .env
```

### 4. Abra o arquivo `.env` e edite as credenciais de conexão

```bash
    DB_USER=postgres
    DB_PASSWORD=sua_senha_do_banco
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=controle_financeiro
```
### 5. Criar o Banco de Dados no PostgreSQL  
Abra o terminal do PostgreSQL ou seu gerenciador (pgAdmin/DBeaver) e crie um banco vazio:
```SQL
    CREATE DATABASE controle_financeiro;
```

### 6. Executar o servidor
Para iniciar a aplicação de forma simplificada, execute:
```bash
    python main.py
```
✅ O servidor estará ativo em: http://127.0.0.1:8000

---

## 🗺️ Guia de Testes e Rotas (Swagger)
Acesse a documentação interativa em: http://127.0.0.1:8000/docs

### Principais Endpoints Disponíveis:
* `POST /finance/transactions`: Registra uma transação (Receita ou Despesa) rodando o Strategy Pattern de categorização e salvando o valor criptografado no banco.

* `GET /finance/transactions`: Retorna o histórico de transações descriptografado em tempo real.

* `POST /finance/goals`: Estabelece limites de teto orçamentário para despesas fixas ou variáveis.

* `GET /finance/summary`: Retorna o saldo líquido atualizado, projeções futuras e dispara uma lista de objetos contendo os Alertas de Estouro caso os limites das metas tenham sido ultrapassados.

---

## 🧪 Testes Automatizados
O projeto conta com testes unitários focados na validação isolada do comportamento e integridade do Design Pattern aplicado.

Para rodar a suíte de testes com segurança de caminhos, utilize o comando:
```bash
    python -m pytest tests/
```
