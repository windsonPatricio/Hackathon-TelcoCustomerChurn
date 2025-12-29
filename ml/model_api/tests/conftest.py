import pytest
from fastapi.testclient import TestClient
from app import app 

# TODO: Verificar a necessidade de mudar o escopo dos fixtures para 'module' ou 'session'.
@pytest.fixture
def client():
    # O TestClient com block lança o evento de startup (lifespan),
    # garantindo que o ModelWrapper seja inicializado.
    with TestClient(app) as c:
        yield c

@pytest.fixture
def sample_payload():
    """
    Retorna um dicionário válido conforme as regras estritas 
    do schemas.py (Enums e validações).
    """
    return {
        "genero": "homem",
        "idoso": 0,
        "parceiro": 1,
        "dependentes": 0,
        "tempo_contrato_meses": 12,
        "servico_telefone": 1,
        "linhas_multiplas": "nao",           # Enum LinhasMultiplas
        "tipo_internet": "fibra",            # Enum TipoInternet
        "seguranca_online": "sim",           # Enum TriStateInternet
        "backup_online": "nao",
        "protecao_dispositivo": "nao",
        "suporte_tecnico": "nao",
        "streaming_tv": "sim",
        "streaming_filmes": "sim",
        "tipo_contrato": "mensal",           # Enum TipoContrato
        "cobranca_digital": 1,
        "metodo_pagamento": "cheque_eletronico", # Enum MetodoPagamento
        "cobranca_mensal": 79.85,
        "cobranca_total": 1200.5
    }