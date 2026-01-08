# GasPot Simulator Dockerfile
# TLS-350 ATG Simulator for ICS/OT training
#
# Simulates a Veeder-Root TLS-350 Automatic Tank Gauge
# with 6 tanks: 3 Natural Gas, 2 Diesel, 1 Water

FROM python:3.11-slim

# Install netcat for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -g 10001 gaspot && \
    useradd -u 10000 -g gaspot -m gaspot

WORKDIR /app

# Copy requirements and install dependencies
COPY --chown=gaspot:gaspot requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=gaspot:gaspot GasPot.py .
COPY --chown=gaspot:gaspot config.ini .

USER gaspot

EXPOSE 10001

CMD ["python", "-u", "GasPot.py"]
