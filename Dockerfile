FROM python:3.12.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements-dev.txt ./

RUN python -m pip install --no-cache-dir -r requirements-dev.txt

RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid 10001 --create-home appuser

COPY --chown=10001:10001 pyproject.toml ./
COPY --chown=10001:10001 asistente/ ./asistente/
COPY --chown=10001:10001 tests/ ./tests/

RUN chown 10001:10001 /app

USER 10001:10001

CMD ["python", "-m", "pytest", "tests/", "--cov=asistente", "--cov-branch", "--cov-report=term-missing", "--cov-report=xml"]
