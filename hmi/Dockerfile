# GasPot HMI Dockerfile
# Flask web dashboard for tank monitoring
#
# Phase 1: Placeholder for validation
# Phase 4: Full implementation

FROM python:3.11-slim

# Install curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -g 10001 hmi && \
    useradd -u 10000 -g hmi -m hmi

WORKDIR /app

# Phase 1: Simple HTTP server placeholder for testing
RUN pip install --no-cache-dir flask

# Create minimal Flask app for health check testing
RUN echo 'from flask import Flask\n\
app = Flask(__name__)\n\
\n\
@app.route("/health")\n\
def health():\n\
    return "OK", 200\n\
\n\
@app.route("/")\n\
def index():\n\
    return "HMI Placeholder - Phase 1", 200\n\
\n\
if __name__ == "__main__":\n\
    app.run(host="0.0.0.0", port=5000)' > /app/placeholder.py

USER hmi

EXPOSE 5000

CMD ["python", "/app/placeholder.py"]
