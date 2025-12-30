import pytest
from fastapi.testclient import TestClient

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_predict_endpoint_success(client, sample_payload):
    response = client.post("/predict", json=sample_payload)
    assert response.status_code == 200
    data = response.json()
    assert "previsao" in data
    assert isinstance(data["probabilidade"], float)

def test_predict_validation_error(client):
    """Testa se o Pydantic barra JSON vazio"""
    response = client.post("/predict", json={})
    assert response.status_code == 422 # Unprocessable Entity

def test_predict_handles_model_crash(client, sample_payload, mocker):
    """
    Simula erro fatal (RuntimeError) vindo do ModelWrapper.
    """
    # Mockamos o método da CLASSE, assim afeta qualquer instância que o app criar
    with mocker.patch("inference.ModelWrapper.predict_single", side_effect=RuntimeError("Falha na Matrix")):
        response = client.post("/predict", json=sample_payload)
        
        assert response.status_code == 500
        assert "Falha na Matrix" in response.json()["detail"]

def test_predict_handles_generic_exception(client, sample_payload, mocker):
    """
    Simula erro não tratado (ex: NullPointer, Divisão por zero).
    Deve retornar mensagem genérica por segurança.
    """
    with mocker.patch("inference.ModelWrapper.predict_single", side_effect=ValueError("Bug Interno Secreto")):
        response = client.post("/predict", json=sample_payload)
        
        assert response.status_code == 500
        # A mensagem pro usuário NÃO deve conter "Bug Interno Secreto"
        assert response.json()["detail"] == "Erro interno ao processar predição."

def test_predict_fails_gracefully_if_model_is_none(client, sample_payload, mocker):
    """
    Simula cenário onde o app iniciou mas o modelo falhou ao carregar (é None).
    """
    # Mockamos a função get_model ou alteramos o state
    # Como usamos app.state, podemos injetar a falha simulando que get_model lança 503
    
    # Opção A: Mockar o app.state (Mais difícil pois o TestClient já iniciou o app)
    # Opção B: Mockar a dependência get_model no app (FastAPI way)
    
    from app import app, get_model
    from fastapi import HTTPException
    
    def override_get_model_fail():
        raise HTTPException(status_code=503, detail="Serviço indisponível simulado")
    
    # Override de dependência do FastAPI
    app.dependency_overrides[get_model] = override_get_model_fail
    
    try:
        response = client.post("/predict", json=sample_payload)
        assert response.status_code == 503
        assert "Serviço indisponível" in response.json()["detail"]
    finally:
        # Limpa o override para não quebrar outros testes
        app.dependency_overrides = {}

def test_batch_failure_behavior(client, sample_payload, mocker):
    """
    Testa comportamento do Batch quando um item falha.
    Como não podemos mudar o Schema, a API deve rejeitar o lote (Fail Fast).
    """
    payloads = [sample_payload, sample_payload]
    
    # Mock: 1º sucesso, 2º falha
    sucesso = {"churn_prediction": 0, "probabilidade": 0.15}
    mocker.patch("inference.ModelWrapper.predict_single", side_effect=[sucesso, RuntimeError("Erro Batch Item 1")])
    
    response = client.post("/predict/batch", json=payloads)
    
    # AGORA ESPERAMOS 500 (Internal Server Error)
    assert response.status_code == 500
    # O detalhe deve explicar onde falhou
    assert "Erro ao processar item 1" in response.json()["detail"]