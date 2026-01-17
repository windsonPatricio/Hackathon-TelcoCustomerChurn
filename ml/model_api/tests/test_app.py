# Teste de Health Check
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["model_loaded"] is True
    # Como forçamos o fallback na fixture client, aqui deve ser 'dummy'
    assert data["model_type"] == "dummy"


# Teste de Sucesso na Previsão
def test_predict_endpoint_success(client, sample_payload):
    response = client.post("/predict", json=sample_payload)
    assert response.status_code == 200
    data = response.json()
    # Verifica campos do PredictResponse
    assert "previsao" in data
    assert "probabilidade" in data
    assert isinstance(data["probabilidade"], float)


def test_predict_validation_error(client):
    """Testa se o Pydantic barra JSON vazio"""
    response = client.post("/predict", json={})
    assert response.status_code == 422  # Unprocessable Entity


# Teste de Crash do Modelo (RuntimeError)
def test_predict_handles_model_crash(client, sample_payload, mocker):
    """
    Aqui precisamos de um patch mais agressivo.
    O 'client' já iniciou o app com o DummyModel.
    Precisamos substituir o método predict_single desse objeto vivo.
    """
    # Recupera a instância viva do wrapper dentro do app
    wrapper = client.app.state.model_wrapper

    # Fazemos patch direto no objeto, não na classe, pois o objeto já existe
    mocker.patch.object(
        wrapper, "predict_single", side_effect=RuntimeError("Falha na Matrix")
    )

    response = client.post("/predict", json=sample_payload)

    assert response.status_code == 500
    assert "Falha na Matrix" in response.json()["detail"]


# Teste de Exceção Genérica
def test_predict_handles_generic_exception(client, sample_payload, mocker):
    wrapper = client.app.state.model_wrapper

    mocker.patch.object(
        wrapper, "predict_single", side_effect=ValueError("Bug Secreto")
    )

    response = client.post("/predict", json=sample_payload)

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro interno ao processar predição."


# Teste: Modelo None (503)
# Esse é chato porque o client fixture já iniciou o app COM modelo.
# Precisamos "quebrar" o estado propositalmente.
def test_predict_fails_gracefully_if_model_is_none(client, sample_payload):
    # Salva o wrapper original
    original_wrapper = client.app.state.model_wrapper

    # Destroi o modelo
    client.app.state.model_wrapper = None

    try:
        response = client.post("/predict", json=sample_payload)
        assert response.status_code == 503
        assert "Serviço de ML indisponível" in response.json()["detail"]
    finally:
        # Restaura para não quebrar outros testes
        client.app.state.model_wrapper = original_wrapper


# Teste Batch
def test_batch_failure_behavior(client, sample_payload, mocker):
    payloads = [sample_payload, sample_payload]

    wrapper = client.app.state.model_wrapper

    # Side effect: 1º sucesso, 2º erro
    sucesso = {"churn_prediction": 0, "probabilidade": 0.15, "top_features": []}

    mocker.patch.object(
        wrapper, "predict_single", side_effect=[sucesso, RuntimeError("Erro Batch 1")]
    )

    response = client.post("/predict/batch", json=payloads)

    assert response.status_code == 500
    assert "Erro ao processar item 1" in response.json()["detail"]
