from enum import StrEnum
from typing import Annotated, Optional, Any
from pydantic import BaseModel, Field, ConfigDict

# Tipos reutilizáveis
Int01 = Annotated[int, Field(ge=0, le=1)] # Inteiro que só aceita 0 ou 1
NonNegInt = Annotated[int, Field(ge=0)] # Inteiro não negativo
NonNegFloat = Annotated[float, Field(ge=0)] # Float não negativo

# ----- Enums (StrEnum) -----
class Genero(StrEnum):
    HOMEM = "homem"
    MULHER = "mulher"

class LinhasMultiplas(StrEnum):
    NAO = "nao"
    SEM_TELEFONE = "sem_telefone"
    SIM = "sim"

class TipoInternet(StrEnum):
    DSL = "dsl"
    FIBRA = "fibra"
    SEM_INTERNET = "sem_internet"

class TriStateInternet(StrEnum):
    NAO = "nao"
    SEM_INTERNET = "sem_internet"
    SIM = "sim"

class TipoContrato(StrEnum):
    DOIS_ANOS = "dois_anos"
    MENSAL = "mensal"
    UM_ANO = "um_ano"

class MetodoPagamento(StrEnum):
    CARTAO_CREDITO_AUTOMATICA = "cartao_credito_automatica"
    CHEQUE_ELETRONICO = "cheque_eletronico"
    CHEQUE_ENVIADO = "cheque_enviado"
    TRANSFERENCIA_BANCARIA_AUTOMATICA = "transferencia_bancaria_automatica"

class Previsao(StrEnum):
    VAI_CANCELAR = "Vai cancelar"
    VAI_CONTINUAR = "Vai continuar"

# ----- Modelos -----
class PredictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid") # Rejeita campos extras não definidos no modelo

    genero: Genero = Field(..., description="Gênero do cliente", json_schema_extra={"example": Genero.HOMEM.value})
    idoso: Int01 = Field(..., description="Cliente é idoso (1 = sim, 0 = não)", json_schema_extra={"example": 0})
    parceiro: Int01 = Field(..., description="Cliente possui parceiro (1=sim,0=nao)", json_schema_extra={"example": 1})
    dependentes: Int01 = Field(..., description="Cliente possui dependentes (1=sim,0=nao)", json_schema_extra={"example": 0})
    tempo_contrato_meses: NonNegInt = Field(..., description="Tempo de contrato em meses", json_schema_extra={"example": 12})
    servico_telefone: Int01 = Field(..., description="Cliente possui servico de telefone (1/0)", json_schema_extra={"example": 1})
    linhas_multiplas: LinhasMultiplas = Field(..., description="Cliente possui linhas    multiplas", json_schema_extra={"example": LinhasMultiplas.NAO.value})
    tipo_internet: TipoInternet = Field(..., description="Tipo de internet", json_schema_extra={"example": TipoInternet.FIBRA.value})
    seguranca_online: TriStateInternet = Field(..., description="Cliente possui segurança online", json_schema_extra={"example": TriStateInternet.SIM.value})
    backup_online: TriStateInternet = Field(..., description="Cliente possui backup online", json_schema_extra={"example": TriStateInternet.NAO.value})
    protecao_dispositivo: TriStateInternet = Field(..., description="Cliente possui proteção de dispositivo", json_schema_extra={"example": TriStateInternet.NAO.value})
    suporte_tecnico: TriStateInternet = Field(..., description="Cliente possui suporte técnico", json_schema_extra={"example": TriStateInternet.NAO.value})
    streaming_tv: TriStateInternet = Field(..., description="Cliente possui streaming de TV", json_schema_extra={"example": TriStateInternet.SIM.value})
    streaming_filmes: TriStateInternet = Field(..., description="Cliente possui streaming de filmes", json_schema_extra={"example": TriStateInternet.SIM.value})
    tipo_contrato: TipoContrato = Field(..., description="Tipo de contrato do cliente", json_schema_extra={"example": TipoContrato.MENSAL.value})
    cobranca_digital: Int01 = Field(..., description="Cliente possui cobrança digital (1=sim,0=nao)", json_schema_extra={"example": 1})
    metodo_pagamento: MetodoPagamento = Field(..., description="Método de pagamento adotado pelo cliente", json_schema_extra={"example": MetodoPagamento.CHEQUE_ELETRONICO.value})
    cobranca_mensal: NonNegFloat = Field(..., description="Cobrança mensal", json_schema_extra={"example": 79.85})
    cobranca_total: NonNegFloat = Field(..., description="Cobrança total", json_schema_extra={"example": 1200.5})

#! Possível extensão futura
class TopFeature(BaseModel):
    model_config = ConfigDict(extra="forbid")
    feature: str = Field(..., description="Nome da feature")
    value: Any = Field(..., description="Valor da feature no cliente")
    importance: Annotated[float, Field(ge=0, le=1)] = Field(..., description="Importância estimada (0..1)")

class PredictResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    previsao: Previsao = Field(..., description="Rótulo em linguagem humana", json_schema_extra={"example": Previsao.VAI_CANCELAR.value})
    probabilidade: Annotated[float, Field(ge=0, le=1)] = Field(..., description="Probabilidade estimada de churn")
    # ! Possível extensão futura
    #churn_prediction: Int01 = Field(..., description="Predição numérica 0/1")
    #top_features: list[TopFeature] = Field(..., description="Até 3 features mais relevantes (simples)", max_items=3)
