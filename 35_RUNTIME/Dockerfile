FROM python:3.14-slim

LABEL org.opencontainers.image.title="AI DevOps Engineer" \
      org.opencontainers.image.description="Community Edition AI/SRE incident investigation runtime" \
      org.opencontainers.image.source="https://github.com/OWNER/REPO" \
      org.opencontainers.image.licenses="Apache-2.0"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY 35_RUNTIME/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY 35_RUNTIME /app/35_RUNTIME
WORKDIR /app/35_RUNTIME

RUN useradd --create-home --uid 10001 runtime \
    && mkdir -p /app/runtime-data \
    && chown -R runtime:runtime /app

USER runtime
EXPOSE 8080
ENTRYPOINT ["/app/35_RUNTIME/ops/docker-entrypoint.sh"]
