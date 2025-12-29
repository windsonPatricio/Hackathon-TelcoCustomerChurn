import pytest
import inspect
from typing import get_origin, get_args, Annotated, Any
from pydantic import ValidationError, BaseModel
from enum import Enum

from schemas import (
    PredictRequest,
    PredictResponse,
    # Não precisamos importar Enums individuais aqui, 
    # pois a introspecção os detectará automaticamente.
)

# ==========================================
# 1. Ferramentas de Introspecção (Metaprogramação)
# ==========================================

def unwrap_annotation(annotation: Any) -> Any:
    """
    Remove wrappers como Annotated[...] ou Optional[...] para expor o tipo real.
    Necessário pois o Pydantic V2 encapsula os tipos em Annotated.
    """
    if get_origin(annotation) is Annotated:
        # Retorna o primeiro argumento (o tipo real), ignorando os metadados do Field
        return get_args(annotation)[0]
    return annotation

def get_enum_fields_from_model(model: type[BaseModel]) -> list[tuple[str, Any]]:
    """
    Varre o modelo Pydantic dinamicamente e retorna todos os casos de teste
    para campos baseados em Enum.
    
    Retorna:
        list[tuple[str, Any]]: Lista de (nome_campo, valor_enum_valido)
    """
    enum_cases: list[tuple[str, Any]] = []
    
    for field_name, field_info in model.model_fields.items():
        annotation = field_info.annotation
        real_type = unwrap_annotation(annotation)
        
        # Verifica se o tipo é uma classe e se é subclasse de Enum
        if inspect.isclass(real_type) and issubclass(real_type, Enum):
            for member in real_type:
                enum_cases.append((field_name, member.value))
                
    return enum_cases

# ==========================================
# 2. Configurações de Teste
# ==========================================

# Campos que sabemos que devem ser estritamente 0 ou 1
# (Poderíamos automatizar isso também procurando por Int01, mas 
# para clareza manteremos explícito por enquanto).
CAMPOS_BINARIOS: list[str] = [
    "idoso", "parceiro", "dependentes", "servico_telefone", "cobranca_digital"
]

# ==========================================
# 3. Testes de Integridade do Payload (Request)
# ==========================================

def test_predict_request_happy_path(sample_payload: dict[str, Any]):
    """
    Garante que um payload completo e válido (Golden Sample) 
    passa sem erros e preserva os valores críticos.
    """
    request = PredictRequest(**sample_payload)
    
    # Verificações de sanidade
    assert request.tempo_contrato_meses == 12
    assert request.tipo_internet == "fibra"
    # Verifica se a coerção de tipos não alterou os dados inesperadamente
    assert isinstance(request.cobranca_total, float)

@pytest.mark.parametrize("campo, valor", get_enum_fields_from_model(PredictRequest))
def test_dynamic_enum_constraints(sample_payload: dict[str, Any], campo: str, valor: Any):
    """
    Teste Dinâmico: Itera sobre TODOS os campos Enum definidos no Schema.
    Verifica se a API aceita cada uma das opções válidas do Enum.
    """
    payload = sample_payload.copy()
    payload[campo] = valor
    
    req = PredictRequest(**payload)
    assert getattr(req, campo) == valor

def test_predict_request_rejects_unknown_enum(sample_payload: dict[str, Any]):
    """
    Garante que valores fora do domínio (ex: 'internet discada') 
    sejam rejeitados imediatamente, antes de chegar ao modelo.
    """
    payload = sample_payload.copy()
    payload["tipo_internet"] = "discada_4g_inexistente"
    
    with pytest.raises(ValidationError) as excinfo:
        PredictRequest(**payload)
    
    errors = excinfo.value.errors()
    assert any(e["loc"] == ("tipo_internet",) for e in errors), "O erro deve apontar para o campo 'tipo_internet'"

# ==========================================
# 4. Testes de Validadores Numéricos (Int01 / Ranges)
# ==========================================

@pytest.mark.parametrize("campo", CAMPOS_BINARIOS)
@pytest.mark.parametrize("valor", [0, 1])
def test_binary_fields_valid_values(sample_payload: dict[str, Any], campo: str, valor: int):
    """Verifica se campos Int01 aceitam estritamente 0 e 1."""
    payload = sample_payload.copy()
    payload[campo] = valor
    req = PredictRequest(**payload)
    assert getattr(req, campo) == valor

@pytest.mark.parametrize("campo", CAMPOS_BINARIOS)
@pytest.mark.parametrize("valor_invalido", [-1, 2, 10, 99])
def test_binary_fields_reject_out_of_bounds(sample_payload: dict[str, Any], campo: str, valor_invalido: int):
    """Verifica se campos Int01 rejeitam valores numéricos fora do range permitido."""
    payload = sample_payload.copy()
    payload[campo] = valor_invalido
    
    with pytest.raises(ValidationError) as excinfo:
        PredictRequest(**payload)
    
    # Verifica se o erro menciona o input inválido
    assert "Input should be" in str(excinfo.value) or "less than or equal to" in str(excinfo.value)

# ==========================================
# 5. Testes de Contrato de Resposta (Response)
# ==========================================

def test_predict_response_structure_compliance():
    """
    Valida se o output da API obedece estritamente o contrato.
    Crucial para garantir que quem consome a API (front ou outro serviço) não quebre.
    """
    data = {
        "previsao": "Vai cancelar",
        "probabilidade": 0.85
    }
    response = PredictResponse(**data)
    assert response.probabilidade == 0.85
    assert response.previsao == "Vai cancelar"

def test_response_type_coercion_robustness():
    """
    Testa a resiliência da serialização.
    Mesmo que o modelo ML retorne um numpy.float ou string numérica,
    o Pydantic deve entregar um float limpo.
    """
    raw_data = {
        "previsao": "Vai cancelar",
        "probabilidade": "0.85"  # Simulando um retorno "sujo" como string
    }
    
    response = PredictResponse(**raw_data)
    
    # 1. Valida valor
    assert response.probabilidade == 0.85
    # 2. Valida tipo estrito (Python puro, não numpy type ou string)
    assert type(response.probabilidade) is float

def test_response_rejects_bad_data_types():
    """
    Garante que se o modelo retornar lixo (ex: NaN, string texto),
    a API lança erro (500 interno) em vez de entregar JSON inválido.
    """
    raw_data = {
        "previsao": "Vai cancelar",
        "probabilidade": "muito_alto_risco" # String não numérica
    }
    
    with pytest.raises(ValidationError) as excinfo:
        PredictResponse(**raw_data)
        
    assert "Input should be a valid number" in str(excinfo.value)