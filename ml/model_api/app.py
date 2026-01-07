from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Depends
import logging

# Imports locais
from schemas import PredictRequest, PredictResponse
from inference import ModelWrapper
from config import LOG_LEVEL

# Configuração de Logs
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("churn_api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de Contexto: Inicializa recursos no startup e limpa no shutdown.
    Armazena o modelo em app.state para evitar globais soltas.
    """
    logger.info("Startup: Inicializando recursos de ML...")
    try:
        # Carrega o modelo e anexa ao estado da aplicação
        # Se ALLOW_MODEL_FALLBACK=False e o arquivo não existir, 
        # isso aqui vai dar raise FileNotFoundError e abortar o startup do Uvicorn.
        # O container morre
        app.state.model_wrapper = ModelWrapper()
        
        mode = "DUMMY" if app.state.model_wrapper.is_dummy else "PROD"
        logger.info(f"Startup Completo. Modo de Operação: [{mode}]")
        
    except Exception as e:
        logger.critical(f"FALHA CRÍTICA NO STARTUP: {e}", exc_info=True)
        # Re-lança a exceção para matar o processo
        raise e
    
    yield
    
    logger.info("Shutdown: Liberando recursos...")
    app.state.model_wrapper = None

app = FastAPI(
    title="ChurnInsight Model API",
    version="v1",
    lifespan=lifespan
)

# --- Dependências ---
def get_model(request: Request) -> ModelWrapper:
    """
    Dependency Injection: Recupera o modelo do estado da aplicação.
    Lança erro imediatamente se o modelo não estiver disponível.
    """
    model = getattr(request.app.state, "model_wrapper", None)
    if model is None:
        logger.error("Tentativa de acesso ao modelo falhou: Modelo não inicializado.")
        raise HTTPException(status_code=503, detail="Serviço de ML indisponível (Modelo não carregado).")
    return model

# --- Endpoints ---

@app.get("/health")
def health():
    """
    Retorna saúde da API e metadados do modelo carregado.
    """
    wrapper = getattr(app.state, "model_wrapper", None)
    
    if wrapper is None:
        # Se chegou aqui, algo muito estranho aconteceu (wrapper sumiu da memória)
        raise HTTPException(status_code=503, detail="Modelo não inicializado")

    return {
        "status": "ok",
        "model_loaded": True,
        "model_type": "dummy" if wrapper.is_dummy else "production",
        "model_version": wrapper.model_version,
        "fallback_enabled": getattr(wrapper, "is_dummy", False) # ou ler de config
    }

@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest, model: ModelWrapper = Depends(get_model)):
    """
    Endpoint unitário.
    Usa Depends(get_model) para garantir que overrides de teste funcionem.
    """
    try:
        features = payload.model_dump()
        result = model.predict_single(features)
        
        return {
            "previsao": "Vai cancelar" if result["churn_prediction"] == 1 else "Vai continuar",
            "probabilidade": result["probabilidade"]
        }
        
    except RuntimeError as rt:
        logger.error(f"Erro de inferência: {rt}")
        raise HTTPException(status_code=500, detail=str(rt))
    except Exception as exc:
        logger.exception("Erro não tratado no endpoint /predict")
        raise HTTPException(status_code=500, detail="Erro interno ao processar predição.")
    
@app.post("/predict/batch", response_model=list[PredictResponse])
def predict_batch(payloads: list[PredictRequest], request: Request):
    """
    Processamento em lote.
    # TODO: Avaliar a implementação de falha parcial não abortar todo o lote.
    NOTA: Em caso de falha parcial, retorna probabilidade -1.0 para indicar erro
    ao cliente consumidor, em vez de mascarar com 0.0.
    """
    model = get_model(request)
    results = []
    
    # TODO: Estudar a necessidade de implementar um previsão sem for loop, usando DataFrame direto.
    for i, p in enumerate(payloads):
        try:
            features = p.model_dump()
            r = model.predict_single(features)
            results.append({
                "previsao": "Vai cancelar" if r["churn_prediction"] == 1 else "Vai continuar",
                "probabilidade": r["probabilidade"]
            })
        # TODO: Estudar a necessidade de mudar o schema
        except Exception as exc:
            logger.error(f"Falha fatal no item {i} do batch: {exc}")
            # Aborta imediatamente. O cliente deve corrigir os dados ou reenviar.
            raise HTTPException(
                status_code=500, 
                detail=f"Erro ao processar item {i} do lote: {str(exc)}"
            )
            
    return results