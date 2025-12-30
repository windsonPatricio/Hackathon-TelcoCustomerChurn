FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Instala dependências do SO e Python (Cache Layer)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 2. Copia o código da API
COPY . .

# 3. Cria usuário e ajusta permissões
#    O chown garante que o usuário consiga ler/escrever em /app se precisar
RUN useradd -m appuser && chown -R appuser /app

USER appuser

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]