from pathlib import Path
import os
from dotenv import load_dotenv

# 1. Definir a Raiz do Projeto
# __file__ = .../model_api/config.py
# parents[0] = .../model_api
# parents[1] = .../ (Raiz do projeto)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# 2. Carregar o .env da raiz
load_dotenv(PROJECT_ROOT / ".env")

# 3. Configurar caminhos
RANDOM_SEED = int(os.getenv("RANDOM_SEED", 25))

# Threshold (Corte) de classificação. Padrão 0.5.
CHURN_THRESHOLD = float(os.getenv("CHURN_THRESHOLD", 0.5))

# O padrão deve ser buscar na pasta 'models' que está na raiz
# TODO: Possivelmente será necessário ajustar isso para produção.
DEFAULT_MODEL_FILENAME = "modelo_churn.joblib"
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / DEFAULT_MODEL_FILENAME

# Se a variável de ambiente existir, usa ela. Se não, usa o caminho construído acima.
model_env = os.getenv("MODEL_PATH")
MODEL_PATH = Path(model_env) if model_env else DEFAULT_MODEL_PATH

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Debug para você ver se ele achou o caminho certo
if __name__ == "__main__":
    print(f"Raiz do projeto: {PROJECT_ROOT}")
    print(f"Procurando modelo em: {MODEL_PATH}")