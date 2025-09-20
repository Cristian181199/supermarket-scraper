# Production API Dockerfile (Versión con Entrypoint)
FROM python:3.11-slim

WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production

# Instalar dependencias del sistema, incluyendo netcat-openbsd para el script de espera
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ curl postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

COPY --chown=appuser:appuser services/api/requirements.txt ./services/api/requirements.txt
COPY --chown=appuser:appuser shared/requirements.txt ./shared/requirements.txt
# Copiamos alembic.ini para que el comando de migración funcione
COPY --chown=appuser:appuser infrastructure/alembic.ini ./infrastructure/alembic.ini

USER appuser
ENV PATH="/home/appuser/.local/bin:${PATH}"

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r services/api/requirements.txt
RUN pip install --no-cache-dir -r shared/requirements.txt
RUN pip install --no-cache-dir gunicorn alembic

# Copiamos todo el código de la aplicación
USER root
COPY --chown=appuser:appuser . .

# Copiamos y damos permisos de ejecución al script de inicio
COPY --chown=appuser:appuser infrastructure/docker/api-entrypoint.prod.sh /usr/local/bin/api-entrypoint.prod.sh
RUN chmod +x /usr/local/bin/api-entrypoint.prod.sh

USER appuser

ENV PYTHONPATH=/usr/src/app
EXPOSE 8000

# Usamos el script como punto de entrada
ENTRYPOINT ["/usr/local/bin/api-entrypoint.prod.sh"]