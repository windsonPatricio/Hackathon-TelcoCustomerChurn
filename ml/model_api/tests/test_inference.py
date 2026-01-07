import pytest
import numpy as np
from inference import ModelWrapper
from model_stub import DummyModel

# ==========================================
# FIXTURES LOCAIS
# ==========================================

@pytest.fixture
def mock_sklearn_model(mocker):
    """
    Cria um Mock que imita um Pipeline treinado do Scikit-Learn.
    Usado para simular o 'modelo real' sem precisar de um arquivo .pkl no disco.
    """
    mock_model = mocker.Mock()
    
    # Simula retorno do predict_proba: [[0.2, 0.8]] (80% chance churn)
    # Shape (1, 2) para 1 amostra
    mock_model.predict_proba.return_value = np.array([[0.2, 0.8]])
    
    # Atributos necessários que o Wrapper pode checar
    mock_model.classes_ = np.array([0, 1])
    
    return mock_model

def test_wrapper_loads_dummy_when_file_missing_AND_fallback_allowed(mocker, sample_payload):
    """
    Cenário DEV: Arquivo não existe, mas ALLOW_MODEL_FALLBACK = True.
    Resultado: Deve carregar o DummyModel e funcionar.
    """
    # 1. Configura ambiente permissivo
    mocker.patch("inference.ALLOW_MODEL_FALLBACK", True)
    mocker.patch("inference.Path.exists", return_value=False)
    
    wrapper = ModelWrapper(model_path="ghost_path.joblib")
    
    # Validações
    assert isinstance(wrapper.model, DummyModel)
    assert wrapper.is_dummy is True
    assert wrapper.model_version == "dummy_stub_v1"
    
    # Predição funciona
    result = wrapper.predict_single(sample_payload)
    assert result["probabilidade"] is not None

def test_wrapper_CRASHES_when_file_missing_AND_fallback_disabled(mocker):
    """
    Cenário PROD (CRÍTICO): Arquivo não existe e ALLOW_MODEL_FALLBACK = False.
    Resultado: Deve lançar FileNotFoundError para derrubar a aplicação.
    """
    # 1. Configura ambiente restrito (Produção)
    mocker.patch("inference.ALLOW_MODEL_FALLBACK", False)
    mocker.patch("inference.Path.exists", return_value=False)
    
    # 2. Verifica se explode o erro correto
    with pytest.raises(FileNotFoundError) as exc:
        ModelWrapper(model_path="ghost_path.joblib")
    
    assert "CRÍTICO: Modelo não encontrado" in str(exc.value)

def test_wrapper_loads_real_model_success(mocker, mock_sklearn_model, sample_payload):
    """
    Cenário IDEAL: Arquivo existe. Configuração de fallback é irrelevante aqui.
    """
    mocker.patch("inference.Path.exists", return_value=True)
    mocker.patch("inference.load", return_value=mock_sklearn_model)
    
    wrapper = ModelWrapper(model_path="real_model.joblib")
    
    assert not isinstance(wrapper.model, DummyModel)
    assert wrapper.is_dummy is False
    assert wrapper.model_version == "production_v1"
    
    result = wrapper.predict_single(sample_payload)
    assert result["churn_prediction"] == 1

def test_wrapper_runtime_error_propagation(mocker, mock_sklearn_model, sample_payload):
    """
    Testa falha DURANTE a predição (não durante o load).
    """
    mocker.patch("inference.Path.exists", return_value=True)
    mocker.patch("inference.load", return_value=mock_sklearn_model)
    
    # O modelo carregou, mas falha ao prever
    mock_sklearn_model.predict_proba.side_effect = ValueError("NaN Values")
    
    wrapper = ModelWrapper(model_path="real_model.joblib")
    
    with pytest.raises(RuntimeError) as exc:
        wrapper.predict_single(sample_payload)
    
    assert "Falha interna no serviço de inferência" in str(exc.value)