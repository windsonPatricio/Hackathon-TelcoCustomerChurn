import pandas as pd
import numpy as np
from model_stub import DummyModel

# ==========================================
# TESTES DO MODELO STUB (Unitários)
# ==========================================


def test_dummy_model_sklearn_compliance():
    """
    Verifica se o Dummy obedece a API padrão do Scikit-Learn.
    Isso garante que ele possa ser substituído pelo modelo real sem quebrar o código.
    """
    model = DummyModel()

    # Deve ter os métodos essenciais de um Estimator/Classifier
    assert hasattr(model, "fit")
    assert hasattr(model, "predict_proba")
    assert hasattr(model, "classes_")

    # Teste de input DataFrame (simulando o pipeline real)
    df = pd.DataFrame([{"tipo_contrato": "mensal", "tempo_contrato_meses": 12}])

    # Deve retornar array (1, 2) -> [[prob_classe_0, prob_classe_1]]
    proba = model.predict_proba(df)

    assert isinstance(proba, np.ndarray)
    assert proba.shape == (1, 2)

    # Probabilidades devem ser válidas e somar 1.0
    assert np.isclose(proba[0, 0] + proba[0, 1], 1.0)
    assert 0.0 <= proba[0, 1] <= 1.0


def test_dummy_logic_determinism():
    """
    Verifica se a mesma seed gera EXATAMENTE o mesmo resultado.
    Crucial para debugging e testes de regressão.
    """
    payload = pd.DataFrame([{"feat": 1}])

    # Instância 1
    m1 = DummyModel(seed=42)
    p1 = m1.predict_proba(payload)[0, 1]

    # Instância 2 (mesma seed)
    m2 = DummyModel(seed=42)
    p2 = m2.predict_proba(payload)[0, 1]

    assert p1 == p2
