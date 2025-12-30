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

# ==========================================
# TESTES DO WRAPPER (Integração de Componente)
# ==========================================

def test_wrapper_loads_dummy_when_file_missing(mocker, sample_payload):
    """
    Cenário: Arquivo de modelo não existe no disco.
    Resultado: Wrapper deve capturar o erro, logar warning e instanciar o Dummy.
    """
    # Mock Path.exists para retornar False
    mocker.patch("inference.Path.exists", return_value=False)
    
    # Tenta carregar de um caminho fantasma
    wrapper = ModelWrapper(model_path="ghost_path.joblib")
    
    # Verifica se o fallback ocorreu
    assert isinstance(wrapper.model, DummyModel)
    
    # Verifica se o predict funciona (usando o dummy)
    result = wrapper.predict_single(sample_payload)
    assert "probabilidade" in result
    assert isinstance(result["probabilidade"], float)

def test_wrapper_loads_real_model_success(mocker, mock_sklearn_model, sample_payload):
    """
    Cenário: Arquivo existe e carrega corretamente.
    Resultado: Wrapper deve usar o modelo carregado (Mock) e não o Dummy.
    """
    # 1. Simula que o arquivo existe
    mocker.patch("inference.Path.exists", return_value=True)
    
    # 2. Simula o load do joblib retornando nosso Mock
    mock_load = mocker.patch("inference.load", return_value=mock_sklearn_model)
    
    wrapper = ModelWrapper(model_path="real_model.joblib")
    
    # Validações
    assert not isinstance(wrapper.model, DummyModel) # Não pode ser Dummy
    assert wrapper.model == mock_sklearn_model       # Deve ser nosso Mock
    
    # Executa predição
    result = wrapper.predict_single(sample_payload)
    
    # Valida se usou o valor do Mock (0.8 definido na fixture)
    assert result["probabilidade"] == 0.8
    assert result["churn_prediction"] == 1 
    
    # Garante que o load foi chamado apenas 1 vez
    mock_load.assert_called_once()

def test_wrapper_handles_corrupted_file(mocker, sample_payload):
    """
    Cenário: Arquivo existe (Path=True) mas está corrompido/incompatível.
    Resultado: Deve capturar a exceção do joblib e fazer fallback para Dummy.
    """
    mocker.patch("inference.Path.exists", return_value=True)
    
    # joblib.load explode com erro (simulando arquivo corrompido)
    mocker.patch("inference.load", side_effect=EOFError("Arquivo incompleto/corrompido"))
    
    wrapper = ModelWrapper(model_path="corrupt.joblib")
    
    # Deve ter feito fallback gracefully
    assert isinstance(wrapper.model, DummyModel)
    
    # Sistema continua funcionando para o usuário final
    result = wrapper.predict_single(sample_payload)
    assert result is not None

def test_wrapper_runtime_error_propagation(mocker, mock_sklearn_model, sample_payload):
    """
    Cenário Crítico: O modelo carregou com sucesso, mas FALHOU durante a execução do predict.
    
    Resultado: Diferente do carregamento, aqui NÃO queremos fallback silencioso.
    Queremos que o erro suba (Bubble up) para causar um HTTP 500, alertando 
    os sistemas de monitoramento (Sentry/Datadog) que o modelo de produção está quebrado.
    """
    mocker.patch("inference.Path.exists", return_value=True)
    mocker.patch("inference.load", return_value=mock_sklearn_model)
    
    # Configura o mock para falhar APENAS na hora da inferência
    mock_sklearn_model.predict_proba.side_effect = ValueError("Input shape mismatch ou NaN values")
    
    wrapper = ModelWrapper(model_path="real_model.joblib")
    
    # Verifica se lança RuntimeError (conforme definido no código do wrapper)
    with pytest.raises(RuntimeError) as exc:
        wrapper.predict_single(sample_payload)
    
    assert "Falha interna no serviço de inferência" in str(exc.value)