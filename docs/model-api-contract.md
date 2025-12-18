# CONTRATO DE INTEGRAÇÃO — Model API (POST /predict)

**Resumo:** este documento define o contrato JSON entre consumidores (backend Java, frontend, etc.) e a Model API que recebe informações de um cliente e retorna uma previsão de churn.  
**Observação importante:** `id_cliente` **NÃO** é enviado para a model-api (não é usado como input do modelo).

- Endpoint: `POST /predict`  
- Content-Type: `application/json`  
- Valores categóricos devem usar exactamente os tokens especificados (lowercase, snake_case) conforme as listas abaixo.

---

## Entrada (request) — Schema obrigatório

**Formato geral (JSON)**

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

> **Regras:**
>
> * Todos os campos acima **devem** estar presentes no JSON enviado.
> * Para campos binários, use `0` ou `1` (inteiro).
> * Para campos categóricos (strings) use os valores **exatos** listados mais abaixo (lowercase, snake_case).
> * Tipos numéricos aceitam inteiros ou floats conforme tabela.

---

## Tabela de campos (descrição + tipos)

| Campo                  | Descrição                               | Tipo (Pandas)        | Tipo (API / Java)  |
| ---------------------- | --------------------------------------- | -------------------- | ------------------ |
| `genero`               | Gênero do cliente                       | `category`           | `String` / `Enum`  |
| `idoso`                | Cliente é idoso (1 = sim, 0 = não)      | `int8`               | `Integer` (0/1)    |
| `parceiro`             | Possui parceiro(a)                      | `int8`               | `Integer` (0/1)    |
| `dependentes`          | Possui dependentes                      | `int8`               | `Integer` (0/1)    |
| `tempo_contrato_meses` | Tempo de contrato em meses              | `int16`              | `Integer`          |
| `servico_telefone`     | Possui serviço de telefone              | `int8`               | `Integer` (0/1)    |
| `linhas_multiplas`     | Possui múltiplas linhas                 | `category`           | `String` / `Enum`  |
| `tipo_internet`        | Tipo de internet contratada             | `category`           | `String` / `Enum`  |
| `seguranca_online`     | Serviço de segurança online             | `category`           | `String` / `Enum`  |
| `backup_online`        | Serviço de backup online                | `category`           | `String` / `Enum`  |
| `protecao_dispositivo` | Proteção de dispositivo                 | `category`           | `String` / `Enum`  |
| `suporte_tecnico`      | Suporte técnico                         | `category`           | `String` / `Enum`  |
| `streaming_tv`         | Serviço de streaming de TV              | `category`           | `String` / `Enum`  |
| `streaming_filmes`     | Serviço de streaming de filmes          | `category`           | `String` / `Enum`  |
| `tipo_contrato`        | Tipo de contrato                        | `category`           | `String` / `Enum`  |
| `cobranca_digital`     | Fatura digital ativa (1 = sim, 0 = não) | `int8`               | `Integer` (0/1)    |
| `metodo_pagamento`     | Método de pagamento                     | `category`           | `String` / `Enum`  |
| `cobranca_mensal`      | Valor mensal cobrado (ex.: 79.85)       | `float32`            | `Float` / `Double` |
| `cobranca_total`       | Valor total cobrado (pode ser `null`)   | `float32` (nullable) | `Float` / `Double` |

---

## Valores permitidos para campos categóricos (tokens exigidos)

* `genero`

  * `homem`
  * `mulher`

* `linhas_multiplas`

  * `nao`
  * `sem_telefone`
  * `sim`

* `tipo_internet`

  * `dsl`
  * `fibra`
  * `sem_internet`

* `seguranca_online`

  * `nao`
  * `sem_internet`
  * `sim`

* `backup_online`

  * `nao`
  * `sem_internet`
  * `sim`

* `protecao_dispositivo`

  * `nao`
  * `sem_internet`
  * `sim`

* `suporte_tecnico`

  * `nao`
  * `sem_internet`
  * `sim`

* `streaming_tv`

  * `nao`
  * `sem_internet`
  * `sim`

* `streaming_filmes`

  * `nao`
  * `sem_internet`
  * `sim`

* `tipo_contrato`

  * `dois_anos`
  * `mensal`
  * `um_ano`

* `metodo_pagamento`

  * `cartao_credito_automatica`
  * `cheque_eletronico`
  * `cheque_enviado`
  * `transferencia_bancaria_automatica`

> **Regra:** valores categóricos são case-sensitive e devem ser enviados exatamente como listados (lowercase, snake_case). A model-api validará e rejeitará valores não listados com HTTP 400.

---

## Saída (response) — Schema

**Formato JSON de sucesso (200 OK):**

```json
{
  "previsao": "Vai cancelar",
  "probabilidade": 0.81
}
```

* `previsao` — string: **"Vai cancelar"** ou **"Vai continuar"**. (Texto legível para apresentação.)
* `probabilidade` — float entre `0.0` e `1.0` representando a probabilidade estimada de churn (valores com duas casas decimais no exemplo, mas enviar float em precisão padrão).

**Notas de design:**

* Internamente o modelo terá threshold|(limiar de decisão) que será determinado durante o desenvolvimento (ex.: 0.5). Se a probabilidade for maior ou igual ao threshold, a previsão será "Vai cancelar", caso contrário "Vai continuar".
---

## Códigos de resposta e comportamento de erro

* `200 OK` — requisição válida, resposta com `previsao` e `probabilidade`.
* `400 Bad Request` — JSON inválido, campos faltando, tipos errados ou valores categóricos não permitidos. Body deve conter mensagem de erro com campo e motivo.
* `422 Unprocessable Entity` — validação Pydantic (ex.: tipo certo mas constraints violadas).
* `500 Internal Server Error` — erro interno; responder com mensagem genérica e `request_id` para rastreio.

---

## Exemplos práticos

### Exemplo de request (com todos os campos obrigatórios)

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

---