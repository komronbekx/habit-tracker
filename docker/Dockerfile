FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .

RUN chmod +x /app/docker/entrypoint.sh

RUN groupadd -r django && useradd -r -g django django \
    && chown -R django:django /app

USER django

EXPOSE 8000

ENTRYPOINT ["docker/entrypoint.sh"]