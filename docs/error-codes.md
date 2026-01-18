# Documentação de Erros na API

Esta API segue um padrão consistente para tratamento de erros, diferenciando **erros de validação**, **erros de integração** e **erros internos**, garantindo previsibilidade para o front-end e robustez na integração com serviços externos (FastAPI).

## Padrão de Resposta de Erro

### Erro genérico

```json
{
  "erro": "Mensagem descritiva do erro" 
}
```

### Erro de validação (campos)

```json
[
  {
    "campo": "nomeDoCampo",
    "mensagem": "Descrição do erro"
  }
]
```

## Tabela de Erros

### 400 - Bad Request

Erro de validação ou JSON inválido.

#### Quando ocorre

- Campos obrigatórios ausentes ou inválidos    
- Violação de regras de Bean Validation (`@NotNull`, `@NotBlank`, etc.)    
- JSON malformado ou incompatível com o contrato da API

#### Exemplo

```json
[
  {
    "campo": "idoso",
    "mensagem": "O campo idoso é obrigatório (0 ou 1)"
  }
]
```

ou

```json
[
  {
    "campo": "idoso",
    "mensagem": "O campo deve ser 0 ou 1"
  }
]
```

### 502 — Bad Gateway

Erro de integração ou contrato inválido com a FastAPI.

Este status pode representar **dois cenários distintos**, tratados separadamente internamente.

#### 1. Erro técnico de integração (`RestClientException`)

##### Quando ocorre

- FastAPI retorna erro HTTP (4xx / 5xx)    
- Timeout ou falha de rede    
- Erro de desserialização    
- Serviço externo inacessível durante a chamada    

###### Resposta

```json
{
  "erro": "Falha na comunicação ou contrato inválido com a API externa."
}
```

#### 2. Resposta inválida da FastAPI (`RespostaInvalidaException`)

##### Quando ocorre

- A FastAPI responde com JSON válido    
- Porém algum campo obrigatório vem como `null`    
- A resposta não pode ser utilizada pela regra de negócio    

##### Exemplo de resposta inválida

```json
{
  "previsao": null,
  "probabilidade": 0.81
}
```

**Resposta**

```json
{
  "erro": "JSON inválido ou incompatível com o contrato da API."
}
```

>**Observação**  
    Qualquer resposta com campos obrigatórios `null` é considerada **contrato inválido** e rejeitada integralmente.

### 503 — Service Unavailable

FastAPI indisponível.

#### Quando ocorre

- Serviço FastAPI fora do ar    
- Falha de conexão (`ConnectException`, `ResourceAccessException`)    

#### Resposta

```json
{
  "erro": "O serviço FastAPI está indisponível no momento."
}
```

### 500 — Internal Server Error

Erro inesperado.

#### Quando ocorre

- Exceções não previstas    
- Falhas internas não mapeadas    

#### Resposta

```json
{
  "erro": "Erro interno inesperado."
}
```
