# GasPot HMI Dockerfile
# Flask web dashboard for tank monitoring
#
# Full implementation with Flask, SQLAlchemy, and TLS-350 client

FROM python:3.11-slim

# Install curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -g 10001 hmi && \
    useradd -u 10000 -g hmi -m hmi

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=hmi:hmi app/ ./app/
COPY --chown=hmi:hmi run.py .

USER hmi

EXPOSE 5000

# Run Flask application
CMD ["python", "run.py"]
