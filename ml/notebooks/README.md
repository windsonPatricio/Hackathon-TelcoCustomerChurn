# ReterMais Churn Experiments

![Python](https://img.shields.io/badge/python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-2.3.3+-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Numpy](https://img.shields.io/badge/numpy-2.4.0+-013243?style=for-the-badge&logo=numpy&logoColor=white)
![PyArrow](https://img.shields.io/badge/pyarrow-22.0.0+-D22128?style=for-the-badge&logo=apache&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit_learn-1.8.0+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![XGBoost](https://img.shields.io/badge/xgboost-3.1.2+-EB4211?style=for-the-badge&logo=xgboost&logoColor=white)
![LightGBM](https://img.shields.io/badge/lightgbm-4.6.0+-3B3B3B?style=for-the-badge&logoColor=white)
![Matplotlib](https://img.shields.io/badge/matplotlib-3.10.8+-11557c?style=for-the-badge&logo=python&logoColor=white)
![Seaborn](https://img.shields.io/badge/seaborn-0.13.2+-4c72b0?style=for-the-badge&logo=python&logoColor=white)
![Statsmodels](https://img.shields.io/badge/statsmodels-0.14.6+-8C1515?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/jupyter_lab-4.5.1+-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

Este repositório armazena os experimentos de Ciência de Dados desenvolvidos para o *Hackathon da Alura*. O ambiente é focado na Análise Exploratória de Dados (EDA), e prototipagem de modelos de Machine Learning para previsão de churn.

## Visão Geral

O projeto visa identificar padrões de cancelamento de clientes e criar modelos preditivos robustos. O fluxo de trabalho é dividido entre a compreensão profunda dos dados e a construção de modelos baseados em árvores de decisão.

## Estrutura do Repositório

```text
.
├── 01_eda.ipynb             # Análise Exploratória e Engenharia de Atributos
├── 02_churn_modeling.ipynb  # Modelagem Preditiva e Avaliação
├── pyproject.toml           # Definição do projeto e dependências
└── uv.lock                  # Arquivo de travamento de versões (lockfile)
└── .python-version          # Versão do Python utilizada
└── README.md                  # Documentação do projeto

```

### Detalhes dos Notebooks

#### 1. Análise Exploratória (01_eda.ipynb)

Focado no entendimento do negócio e preparação dos dados:

* **Saneamento:** Limpeza e padronização de tipos de dados.
* **Estatística:** Análises univariadas, bivariadas e testes de hipóteses (Qui-Quadrado, V de Cramér).
* **Multicolinearidade:** Análise de correlação e VIF (Variance Inflation Factor).
* **Output:** Exportação da base processada em formato Parquet para eficiência.

#### 2. Modelagem Preditiva (02_churn_modeling.ipynb)

Focado no treinamento e validação dos algoritmos:

* **Input:** Carregamento otimizado dos dados processados via PyArrow.
* **Modelos:** Treinamento com XGBoost, LightGBM e modelos nativos do Scikit-learn.
* **Validação:** Estratégias de validação cruzada e análise de métricas de classificação.
*  **Serialização:** Salvamento do pipeline final para implantação futura.

---

## Stack Tecnológico

As versões foram definidas para garantir reprodutibilidade e performance (conforme `pyproject.toml`):

* **Python:** >= 3.11.11
* **Gerenciador de Pacotes:** uv

| Categoria | Biblioteca | Versão Mínima |
| --- | --- | --- |
| **ML & Boosting** | LightGBM, XGBoost, Scikit-learn | 4.6+, 3.1+, 1.8+ |
| **Manipulação** | Pandas, Numpy, PyArrow | 2.3+, 2.3, 22.0+ |
| **Visualização** | Matplotlib, Seaborn | 3.10+, 0.13+ |
| **Estatística** | Statsmodels | 0.14+ |

---

## Instalação e Configuração

Este projeto utiliza o **uv** para gerenciamento de dependências e ambientes virtuais, garantindo uma instalação extremamente rápida.

### 1. Pré-requisitos

Certifique-se de ter o `uv` instalado no seu sistema.

* [Guia de instalação oficial do uv](https://docs.astral.sh/uv/getting-started/installation/)

### 2. Configuração do Ambiente

Navegue até o diretório raiz do projeto e sincronize as dependências. O comando abaixo criará o ambiente virtual e instalará tudo o que é necessário (incluindo o kernel do Jupyter).

```bash
uv sync

```

## Como Executar

Para iniciar os notebooks utilizando o ambiente isolado gerenciado pelo `uv`, utilize um dos comandos abaixo:

**Para Jupyter Notebook clássico:**

```bash
uv run jupyter notebook

```

**Para Jupyter Lab:**

```bash
uv run jupyter lab

```