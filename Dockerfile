FROM python:3.11-slim

WORKDIR /app

# system deps (for bs4 lxml, etc.)
RUN apt-get update && apt-get install -y build-essential libxml2-dev libxslt1-dev libssl-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

RUN mkdir -p /app/data /app/logs /app/data/exports

ENV PYTHONUNBUFFERED=1
ENV DB_PATH=/app/data/prices.db

VOLUME ["/app/data", "/app/logs"]

CMD ["python", "main.py", "--once"]
