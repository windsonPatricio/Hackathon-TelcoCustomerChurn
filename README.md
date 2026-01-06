# Solução Reter+

## Descrição
Este projeto caracteriza-se como uma solução voltada à previsão de cancelamentos de serviços de assinatura (*Churn Prediction*). O repositório contém o código-fonte das APIs de back-end (Java e FastAPI/Python) que, integradas, geram estimativas de cancelamento de um cliente com base nos dados fornecidos.

## Contrato de Integração - Model API
[Acesse a documentação do contrato aqui](https://github.com/windsonPatricio/Hackathon-TelcoCustomerChurn/blob/ml/feature-model-api/docs/model-api-contract.md)

## Back-End

* **Linguagem:** Java 21
* **Framework:** Spring Boot 3.3.x

### Dependências
* **Spring Boot Starter Web:** (MVC e Tomcat)
* **Spring Boot Starter Validation:** (Bean Validation / Hibernate Validator)
* **Spring Boot DevTools:** (Hot reload)
* **Lombok:** (Redução de boilerplate)

## Endpoints

### 1. Previsão de Cancelamento

Gera a requisição de previsão de cancelamento para o modelo de predição.

* **URL:** `/reter/prever`
* **Método:** `POST`
* **Content-Type:** `application/json`

#### Exemplo de Request (com todos os campos obrigatórios)

```json
{
  "genero": "homem",
  "idoso": 0,
  "parceiro": 1,
  "dependentes": 0,
  "tempo_contrato_meses": 12,
  "servico_telefone": 1,
  "linhas_multiplas": "nao",
  "tipo_internet": "fibra",
  "seguranca_online": "sim",
  "backup_online": "nao",
  "protecao_dispositivo": "nao",
  "suporte_tecnico": "nao",
  "streaming_tv": "sim",
  "streaming_filmes": "sim",
  "tipo_contrato": "mensal",
  "cobranca_digital": 1,
  "metodo_pagamento": "cheque_eletronico",
  "cobranca_mensal": 79.85,
  "cobranca_total": 1200.50
}
```
### Exemplo de response (sucesso)

```json
{
  "previsao": "Vai cancelar",
  "probabilidade": 0.81
}
```
### Exemplo de erro



## Validações implementadas:

Todos os campos da requisição são obrigatórios. Desta forma, usa-se notações do pacote BeanValidation
nas camadas de dto, service e controller. Assegurando que todo fluxo de informações é validado. 

## Como utilizar o back-end

1. Realize a clonagem do repositorio:
```
https://github.com/windsonPatricio/Hackathon-TelcoCustomerChurn.git
```
2. Preencha os campos do exemplo de request:

```json
{
  "genero": "homem",
  "idoso": 0,
  "parceiro": 1,
  "dependentes": 0,
  "tempo_contrato_meses": 12,
  "servico_telefone": 1,
  "linhas_multiplas": "nao",
  "tipo_internet": "fibra",
  "seguranca_online": "sim",
  "backup_online": "nao",
  "protecao_dispositivo": "nao",
  "suporte_tecnico": "nao",
  "streaming_tv": "sim",
  "streaming_filmes": "sim",
  "tipo_contrato": "mensal",
  "cobranca_digital": 1,
  "metodo_pagamento": "cheque_eletronico",
  "cobranca_mensal": 79.85,
  "cobranca_total": 1200.50
}
```

3. Realize uma requisição POST para a URL: 
```
http://localhost:8080/reter/prever
```
