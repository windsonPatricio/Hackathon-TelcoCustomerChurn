# Solução Reter+

## Descrição
Este projeto caracteriza-se como uma solução voltada à previsão de cancelamentos de serviços de assinatura (*Churn Prediction*). O repositório contém o código-fonte das APIs de back-end (Java e FastAPI/Python) que, integradas, geram estimativas de cancelamento de um cliente com base nos dados fornecidos.

## Contrato de Integração - Model API
[Acesse a documentação do contrato aqui](https://github.com/windsonPatricio/Hackathon-TelcoCustomerChurn/blob/ml/feature-model-api/docs/model-api-contract.md)

## Back-End

* **Linguagem:** Java 21
* **Framework:** Spring Boot 4.0.0

### Dependências
* **Spring Boot Starter Web:** (MVC e Tomcat)
* **Spring Boot Starter Validation:** (Bean Validation / Hibernate Validator)
* **Spring Boot DevTools:** (Hot reload)

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

## Como utilizar o back-end na sua IDE

1. Realize a clonagem do repositorio:
```
https://github.com/windsonPatricio/Hackathon-TelcoCustomerChurn.git
```

2. Em sua IDE favorita, execute o arquivo:

```
../IdeaProjects/Hackathon-TelcoCustomerChurn/api-backend/src/main/java/br/com/retermais/ReterMaisApplication.java
```

3. Preencha os campos do exemplo de request:

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

4. Realize uma requisição POST para a URL:
```
http://localhost:8080/reter/prever
```
## Como utilizar o back-end através do docker

### Execução via Docker Compose

A forma mais simples de rodar a solução completa (**Backend + ML**) é utilizando o Docker Compose.

### Pré-requisitos

* [Docker](https://www.docker.com/) & Docker Compose instalados e rodando.

### Passo a Passo

1. **Clone o repositório:**

```bash
git clone https://github.com/windsonPatricio/Hackathon-TelcoCustomerChurn.git

```

2. **Navegue até o diretório raiz do projeto:**

```bash
cd Hackathon-TelcoCustomerChurn

```

3. **Execute o Docker Compose:**

```bash
docker compose up --build

```

> **Nota:** *Este comando irá construir a imagem do serviço Python (ML) e compilar/subir a aplicação Java (Backend).*

4. **Acesse as APIs:**

Após a inicialização, os serviços estarão disponíveis nas seguintes portas:

* **Backend Java (Principal):** `http://localhost:8080`   (Se estiver exposta no `docker-compose.yml`)
* **Model API (Interna):** `http://localhost:8000`

---
