FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# 3.13: ensure modern build tooling
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir gunicorn

COPY . .

# Create a data dir for SQLite; copy root main.db on first run if present
RUN mkdir -p /app/data
EXPOSE 8080
ENV GUNICORN_APP=run_server:app
ENV DATABASE_URL=sqlite:///main.db

CMD ["bash", "-lc", "test -f main.db || ( [ -f main.db ] && cp main.db /app/data/main.db || true ); exec gunicorn --bind 0.0.0.0:8080 \"${GUNICORN_APP}\" --workers 3 --timeout 60"]
