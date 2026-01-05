# ReterMais Churn Experiments

Este diretório contém os experimentos de Ciência de Dados para o Hackathon ReterMais (Telco Customer Churn). O foco deste ambiente é a Análise Exploratória de Dados (EDA) e a prototipagem de modelos de Machine Learning.

## Estrutura do Projeto

* **01_eda.ipynb**: Notebook focado na análise exploratória. Inclui:
    * Limpeza e padronização de dados.
    * Análises univariadas e bivariadas.
    * Testes de hipóteses (Qui-Quadrado, V de Cramér).
    * Análise de correlação e multicolinearidade (VIF).
    * Prototipagem de Feature Engineering.
    * Exportação dos dados processados em formato Parquet.

* **02_churn_modeling.ipynb**: Notebook focado na modelagem preditiva. Inclui:
    * Carregamento dos dados processados.
    * Treinamento de modelos (XGBoost, LightGBM, Scikit-learn).
    * Avaliação de métricas e validação cruzada.

* **pyproject.toml / uv.lock**: Arquivos de configuração de dependências gerenciados pelo `uv`.

## Pré-requisitos e Instalação

Este projeto utiliza o gerenciador de pacotes `uv` e requer Python 3.11 ou superior.

1. Instale o uv: https://docs.astral.sh/uv/getting-started/installation/

2. Navegue até este diretório e instale as dependências:

```bash
uv sync

```

Este comando criará o ambiente virtual e instalará todas as bibliotecas necessárias listadas no `pyproject.toml`, incluindo as dependências de desenvolvimento (ipykernel).

## Como Executar

Para iniciar o servidor do Jupyter utilizando o ambiente virtual gerenciado pelo `uv`, execute:

```bash
uv run jupyter notebook

```

Ou, se preferir o Jupyter Lab:

```bash
uv run jupyter lab

```

## Dependências Principais

As principais bibliotecas utilizadas neste ambiente são:

* **Manipulação de Dados**: pandas, numpy, pyarrow
* **Visualização**: matplotlib, seaborn
* **Estatística e EDA**: statsmodels
* **Machine Learning**: scikit-learn, xgboost, lightgbm
