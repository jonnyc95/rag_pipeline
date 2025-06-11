# Basis-Image mit Python
FROM python:3.10-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Systemabhängigkeiten installieren
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt ins Image kopieren und installieren
COPY requirements.txt .
RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

# gesamten Code kopieren
COPY . .

# Environment-Variable für besseres Logging
ENV PYTHONUNBUFFERED=1

# Startbefehl für den Container
CMD ["python", "main.py"]
