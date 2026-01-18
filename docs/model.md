# Performance do Modelo (Data Science)

O modelo foi treinado utilizando o dataset clássico **Telco Customer Churn**, passando por etapas de limpeza, análise exploratória, treinamento e seleção de modelos.

### Resultados (Dados de Teste)

Abaixo, o desempenho do modelo nos dados de teste, com foco na classe de interesse (**Churn = Sim**):

| Métrica | Resultado | Significado para o Negócio |
| --- | --- | --- |
| **Recall** | **80%** | *("De todos que saíram, quantos o modelo detectou?")* A métrica mais crítica: garante que a maioria dos clientes em risco seja identificada, minimizando a perda silenciosa de receita. |
| **Precision** | **50%** | *("De quem alertamos que sairia, quantos realmente saíram?")* Indica a eficiência do alerta. Neste caso, para cada 2 alertas gerados, 1 é um churn real. |
| **F1-Score** | **62%** | O equilíbrio harmônico entre precisão e recall, utilizado para comparar a robustez geral do modelo na classe minoritária. |

> **Recursos Técnicos Adicionais:**
> * **Documentação e Ambiente:** Para configuração de dependências, arquitetura e metodologia, acesse o [README Técnico](../ml/notebooks/README.md).
> * **Análise de Dados:** Estudo visual das variáveis e hipóteses de negócio no notebook de [Análise Exploratória (EDA)](../ml/notebooks/01_eda.ipynb).
> * **Modelagem:** Pipeline completo de treinamento e validação no notebook de [Modelagem](../ml/notebooks/02_churn_modeling.ipynb).

---

## Detalhamento da Avaliação: Random Forest

### Matriz de Métricas por Classe

| Métrica | Classe 0 (Não) | Classe 1 (Sim - Churn) | Média Ponderada |
| :--- | :---: | :---: | :---: |
| **Precision** | 0.91 | **0.50** | 0.80 |
| **Recall** | 0.71 | **0.80** | 0.74 |
| **F1-Score** | 0.80 | **0.62** | 0.75 |
| **Support** | 1552 | **561** | 2113 |

 ### Análise de Desempenho

- **Alta Sensibilidade (Recall de 0.80):** Este é o ponto forte do modelo. Ele está identificando corretamente **80%** de todos os clientes que realmente iriam cancelar. Para uma estratégia de retenção, isso é excelente, pois minimiza a perda de clientes por "cegueira" do modelo (Falsos Negativos).
- **O Custo da Precisão (Trade-off):** A precisão de **0.50** na classe de interesse (Yes) indica que, de cada 2 clientes que o modelo aponta como "Risco de Churn", apenas 1 realmente sairia. O outro é um alarme falso. Isso é aceitável se o custo da ação de retenção (ex: enviar um e-mail) for baixo, mas pode ser caro se envolver descontos agressivos.
- **Comparativo de Classes:** O modelo é muito "confiante" para dizer que alguém vai ficar (Precision 0.91), mas mais "ansioso" para dizer que alguém vai sair. Isso sugere que as fronteiras de decisão para a classe minoritária ainda têm sobreposição com a classe majoritária.

---

## Especificações Técnicas do Pipeline

A arquitetura do modelo final utiliza um pipeline composto por tratamento de dados robusto e um classificador Random Forest ajustado para evitar overfitting.

### 1. Pré-processamento

* **Variáveis Numéricas:**
    * **Imputação:** Mediana (`SimpleImputer(strategy='median')`).
    * **Escalonamento:** `RobustScaler`, escolhido para reduzir a influência de outliers presentes nas métricas financeiras.
* **Variáveis Categóricas:**
    * **Codificação:** `OneHotEncoder` com `drop='if_binary'` para evitar colunas redundantes e `handle_unknown='ignore'` para robustez em produção.

### 2. Hiperparâmetros do Modelo

O classificador foi configurado com pesos balanceados para lidar com o desequilíbrio das classes e profundidade limitada para garantir generalização.

```python
RandomForestClassifier(
    n_estimators=300,          # Aumento da estabilidade com mais arvores
    max_depth=5,               # Poda agressiva para evitar overfitting
    min_samples_split=50,      # Regra conservadora para criar novos nos
    min_samples_leaf=20,       # Garante folhas com representatividade estatistica
    class_weight="balanced",   # Penaliza erros na classe minoritaria (Churn)
    criterion="gini",
    n_jobs=-1
)
