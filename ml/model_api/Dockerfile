# -------------------------------------------------------------------
# ETAPA 1: Builder (Apenas gera o .venv com dependências)
# -------------------------------------------------------------------
FROM python:3.11-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:0.6.3 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# 1. Copiamos APENAS os arquivos de dependência primeiro.
# Isso garante que o cache do Docker só quebre se mudar as bibliotecas,
# e não quando mudar o código do app.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-install-project

# -------------------------------------------------------------------
# ETAPA 2: Runner (Imagem final leve)
# -------------------------------------------------------------------
FROM python:3.11-slim-bookworm

WORKDIR /app

# Usuário de segurança
RUN groupadd -r mluser && useradd -r -g mluser mluser

# 1. Copia o ambiente virtual pronto do Builder
COPY --from=builder /app/.venv /app/.venv

# 2. Adiciona ao PATH para não precisar digitar o caminho completo
ENV PATH="/app/.venv/bin:$PATH"

# 3. Copia o código fonte (Agora sim copiamos os arquivos)
COPY . /app

# Permissões
RUN chown -R mluser:mluser /app

USER mluser

EXPOSE 8000

# Como o binário está no PATH (passo 2), podemos chamar direto.
# Usamos "python -m fastapi" que é mais seguro contra erros de path do binário.
CMD ["/app/.venv/bin/fastapi", "run", "app.py", "--port", "8000", "--host", "0.0.0.0"]