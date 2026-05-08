# cognitive-bias-tester backend — multi-stage (builder → dev → production)

FROM python:3.12.3-slim AS builder
WORKDIR /app
ENV PIP_NO_CACHE_DIR=1
RUN pip install --no-cache-dir --upgrade pip
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir --prefix=/install .

FROM python:3.12.3-slim AS dev
WORKDIR /app
ENV PIP_NO_CACHE_DIR=1
RUN apt-get update \
  && apt-get install -y --no-install-recommends curl \
  && rm -rf /var/lib/apt/lists/*
COPY --from=builder /install /usr/local
COPY pyproject.toml ./
COPY src ./src
COPY alembic.ini ./
COPY alembic ./alembic
RUN pip install --no-cache-dir ".[dev]"
EXPOSE 8000

FROM python:3.12.3-slim AS production
WORKDIR /app
ENV PIP_NO_CACHE_DIR=1
RUN apt-get update \
  && apt-get install -y --no-install-recommends curl \
  && rm -rf /var/lib/apt/lists/*
COPY --from=builder /install /usr/local
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
COPY --chown=appuser:appuser alembic.ini ./
COPY --chown=appuser:appuser alembic ./alembic
COPY --chown=appuser:appuser src/ ./src/
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/v1/health || exit 1
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
