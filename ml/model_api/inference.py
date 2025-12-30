import logging
from pathlib import Path
from typing import Any, Optional
import pandas as pd
import numpy as np
from joblib import load

from config import MODEL_PATH, CHURN_THRESHOLD
from model_stub import DummyModel

logger = logging.getLogger(__name__)

class ModelWrapper:
    """
    Controlador responsável pelo ciclo de vida da inferência.
    Abstrai se o modelo subjacente é um Pipeline complexo ou um DummyModel.
    """

    def __init__(self, model_path: Optional[Path] = None, threshold: float = CHURN_THRESHOLD) -> None:
        self.model_path = Path(model_path) if model_path else Path(MODEL_PATH)
        self.threshold = threshold
        self.model = self._load_model()

    def _load_model(self) -> Any:
        """
        Carrega modelo do disco ou inicializa fallback.
        Retorna um objeto compatível com a interface Scikit-Learn.
        """
        if self.model_path.exists():
            try:
                logger.info(f"Carregando modelo de produção: {self.model_path}")
                model = load(self.model_path)
                logger.info("Modelo carregado com sucesso.")
                return model
            except Exception as e:
                logger.error(f"Arquivo encontrado mas corrompido: {e}. Iniciando Fallback.")
        else:
            logger.warning(f"Modelo não encontrado em {self.model_path}. Iniciando Fallback.")

        return DummyModel()

    def _features_to_df(self, features: dict[str, Any]) -> pd.DataFrame:
        """
        Converte o payload (dict) em DataFrame de 1 linha.
        Necessário pois Pipelines Sklearn esperam DataFrames com nomes de colunas.
        """
        return pd.DataFrame([features])

    def predict_single(self, features: dict[str, Any]) -> dict[str, Any]:
        """
        Executa o pipeline de predição completo.
        
        Fluxo:
        dict -> DataFrame -> Predict Proba -> Aplica Threshold -> Formata Resposta
        """
        try:
            # 1. Preparação dos dados
            X_input = self._features_to_df(features)
            
            # 2. Inferência (Polimorfismo: funciona para Dummy ou Real)
            # Retorna array shape (1, 2) -> [[prob_classe_0, prob_classe_1]]
            proba_array = self.model.predict_proba(X_input)
            
            # Pega a probabilidade da classe positiva (1 = Churn)
            prob_churn = float(proba_array[0, 1])
            
            # 3. Regra de Decisão (Thresholding)
            prediction = 1 if prob_churn >= self.threshold else 0
            
            # 4. Explicabilidade (Opcional)
            # Se o modelo tiver método customizado top_features (como o Dummy), usa.
            # Se for um pipeline padrão sklearn, retorna lista vazia (ou implementaria SHAP aqui)
            # TODO: Verificar a implementação de explicabilidade para modelos reais
            top_features = []
            if hasattr(self.model, "top_features"):
                top_features = self.model.top_features(features, k=3)
            
            return {
                "probabilidade": round(prob_churn, 4),
                "churn_prediction": prediction,
                "top_features": top_features
            }

        except Exception as exc:
            # Se falhar no predict do modelo real, isso é crítico.
            logger.critical(f"Falha na inferência: {exc}", exc_info=True)
            raise RuntimeError("Falha interna no serviço de inferência.") from exc