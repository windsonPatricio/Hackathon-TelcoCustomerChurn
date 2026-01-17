import numpy as np
import pandas as pd
from typing import Any
from sklearn.base import BaseEstimator, ClassifierMixin

# Imports relativos
from config import RANDOM_SEED


# Implementação de um custom DummyModel que herda classes do scikit-learn
class DummyModel(BaseEstimator, ClassifierMixin):
    """
    Modelo heurístico (regras fixas) para simular predições de churn.
    Não requer treinamento e é determinístico baseado em uma seed.
    """

    def __init__(self, seed: int = RANDOM_SEED) -> None:
        self.seed = RANDOM_SEED
        self.rng = np.random.default_rng(self.seed)
        self.classes_ = np.array([0, 1])  # Classes possíveis: 0 (no churn), 1 (churn)

    def fit(self, X: Any, y: Any = None):
        """
        No-op (Não faz nada). DummyModel não precisa de treinamento.
        Existe apenas para compatibilidade com scikit-learn.
        """
        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Retorna array (N_samples, 2) igual a um classificador real.
        Coluna 0: Probabilidade de classe 0
        Coluna 1: Probabilidade de classe 1
        """
        # Garante que X é um DataFrame para facilitar acesso as colunas
        if not isinstance(X, pd.DataFrame):
            # Fallback: tenta converter
            X = pd.DataFrame(X)

        n_samples = len(X)

        # Gera probalidades base aleatórias
        base_probs = self.rng.random(n_samples)

        # --- Regras de Negócio (Heurísticas) ---
        # Regra 1: Contrato Mensal aumenta risco
        if "tipo_contrato" in X.columns:
            # Vetorização pandas (muito mais rápido que for loop)
            mask_mensal = X["tipo_contrato"] == "mensal"
            base_probs[mask_mensal] = np.minimum(1.0, base_probs[mask_mensal] + 0.15)

        # Regra 2: Tempo de casa diminui risco
        if "tempo_contrato_meses" in X.columns:
            # Normaliza tenure (assumindo max ~72 meses)
            tenure_factor = X["tempo_contrato_meses"].fillna(0) / 200.0
            base_probs = np.maximum(0.0, base_probs - tenure_factor)

        # Monta o array de saída (N, 2)
        # Coluna 0 (Não Churn) = 1 - p
        # Coluna 1 (Churn) = p
        return np.vstack([1 - base_probs, base_probs]).T

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Retorna classe 0 ou 1 baseado em threshold 0.5 padrão"""
        probs = self.predict_proba(X)[:, 1]
        return (probs >= 0.5).astype(int)

    def top_features(self, X: dict[str, Any], k: int = 3) -> list[dict[str, Any]]:
        """
        Método extra (não padrão sklearn) para explicabilidade.
        """
        candidates = []

        # Simula importância baseada nas regras que definimos acima
        if X.get("tipo_contrato") == "mensal":
            candidates.append(
                {"feature": "tipo_contrato", "value": "mensal", "importance": 0.45}
            )

        tenure = X.get("tempo_contrato_meses", 0)
        if tenure > 0:
            candidates.append(
                {"feature": "tempo_contrato_meses", "value": tenure, "importance": 0.35}
            )

        # Preenche com ruído se faltar
        while len(candidates) < k:
            feat_name = f"fator_aleatorio_{len(candidates)}"
            val = round(self.rng.uniform(0.01, 0.1), 3)
            candidates.append({"feature": feat_name, "value": "N/A", "importance": val})

        return sorted(candidates, key=lambda x: x["importance"], reverse=True)[:k]
