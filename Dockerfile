FROM python:3.11-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1     MODEL_DIR=/opt/model     PORT=8080
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends     curl     jq && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY artifacts ${MODEL_DIR}

EXPOSE 8080
HEALTHCHECK --interval=20s --timeout=3s --retries=3 CMD curl -fsS http://localhost:8080/health || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
