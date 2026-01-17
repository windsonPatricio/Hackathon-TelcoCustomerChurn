# Model API

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128+-009688.svg?logo=fastapi&logoColor=white)
![Manager](https://img.shields.io/badge/uv-0.6.3-purple)
![Status](https://img.shields.io/badge/Status-Active-success)

## Sobre o Projeto

Este é o microserviço de **Inferência de Machine Learning** do projeto. Ele é responsável por carregar o modelo preditivo de Churn (ou um *Dummy Model* de fallback) e expor endpoints REST de alta performance via FastAPI.

O serviço recebe os dados cadastrais e de uso do cliente e retorna a probabilidade dele cancelar o serviço (Churn).

### Funcionalidades

* **Carregamento Seguro:** Utiliza o ciclo de vida (`lifespan`) do FastAPI para carregar o modelo na memória apenas na inicialização, evitando I/O a cada requisição.
* **Fallback Automático:** Se o modelo treinado (`models/modelo_churn.joblib`) não for encontrado, o sistema sobe automaticamente um `DummyModel` (baseado em regras heurísticas/aleatórias) para garantir que a API continue funcional durante o desenvolvimento.
* **Validação Rigorosa:** Contratos de dados garantidos via Pydantic (`schemas.py`), prevenindo erros de tipo antes que cheguem ao modelo.

---

## Como Rodar

### Pré-requisitos

* Python 3.11+
* astral uv (Gerenciador de pacotes)
* Docker (Opcional)

### 1. Desenvolvimento Local (com uv)

Este projeto utiliza `uv` para gerenciamento de dependências e ambientes virtuais.

```bash
# 1. Instalar dependências (cria o .venv automaticamente)
uv sync

# 2. Rodar a API localmente
uv run fastapi run app.py --port 8000

```

### 2. Rodando com Docker

Se preferir rodar em container isolado (recomendado para produção):

```bash
# 1. Build da imagem (estando na pasta model_api)
docker build -t churn-api:v1 .

# 2. Rodar o container
docker run -p 8000:8000 churn-api:v1

```

---

## Contrato da API (Endpoints)

### 1. Health Check

Verifica se a API está online e qual modelo está ativo na memória.

* **GET** `/health`
* **Response:**

```json
{
  "status": "ok",
  "model_loaded": true,
  "model_type": "production",
  "model_version": "production_v1",
  "fallback_enabled": false
}

```

*(Nota: `model_type` retornará "Dummy/Stub Model" se o arquivo .joblib não for encontrado e o fallback estiver ativado)*

### 2. Predição de Churn

Endpoint principal para inferência. Recebe as features do cliente e retorna a previsão.

* **POST** `/predict`
* **Content-Type:** `application/json`

#### Exemplo de Request (Payload)

```json
{
  "genero": "homem",
  "idoso": 0,
  "parceiro": 1,
  "dependentes": 0,
  "tempo_contrato_meses": 12,
  "servico_telefone": 1,
  "linhas_multiplas": "nao",
  "tipo_internet": "fibra",
  "seguranca_online": "sim",
  "backup_online": "nao",
  "protecao_dispositivo": "nao",
  "suporte_tecnico": "nao",
  "streaming_tv": "sim",
  "streaming_filmes": "sim",
  "tipo_contrato": "mensal",
  "cobranca_digital": 1,
  "metodo_pagamento": "cheque_eletronico",
  "cobranca_mensal": 79.85,
  "cobranca_total": 1200.50
}

```

#### Exemplo de Response

```json
{
  "previsao": "Vai cancelar",
  "probabilidade": 0.7845
}

```

---

## Testes

O projeto inclui uma suíte de testes automatizados utilizando `pytest` para garantir a integridade dos schemas e da lógica de inferência.

```bash
# Rodar todos os testes
uv run pytest

# Rodar com output detalhado
uv run pytest -vv

```

---

## Estrutura do Código

```text
.
├── app.py             # Entrypoint FastAPI, rotas e ciclo de vida
├── config.py          # Configurações globais e variáveis de ambiente
├── inference.py       # Wrapper do modelo (Carrega joblib e prepara DataFrame)
├── model_stub.py      # Dummy Model para fallback (testes sem modelo real)
├── schemas.py         # Modelos Pydantic (Input/Output validation)
├── models/            # Diretório onde o arquivo .joblib deve ficar
├── tests/             # Testes unitários e de integração
├── Dockerfile         # Configuração da imagem Docker otimizada (Multi-stage)
└── pyproject.toml     # Dependências do projeto (uv)

```
