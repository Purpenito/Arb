FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./
COPY scripts/api-entrypoint.sh /app/scripts/api-entrypoint.sh
RUN pip install --no-cache-dir -e .
CMD ["/app/scripts/api-entrypoint.sh"]
