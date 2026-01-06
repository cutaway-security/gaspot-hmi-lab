# GasPot Simulator Dockerfile
# TLS-350 ATG Simulator for ICS/OT training
#
# Phase 1: Placeholder for validation
# Phase 2: Full implementation

FROM python:3.11-slim

# Install netcat for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -g 10001 gaspot && \
    useradd -u 10000 -g gaspot -m gaspot

WORKDIR /app

# Placeholder: Copy files when they exist
# COPY --chown=gaspot:gaspot requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY --chown=gaspot:gaspot . .

# Phase 1: Simple TCP listener placeholder for testing
RUN echo '#!/bin/bash\necho "GasPot placeholder - Phase 1"\nwhile true; do echo -e "HTTP/1.1 200 OK\r\n\r\nGasPot Placeholder" | nc -l -p 10001 -q 1; done' > /app/placeholder.sh && \
    chmod +x /app/placeholder.sh

USER gaspot

EXPOSE 10001

CMD ["/bin/bash", "/app/placeholder.sh"]
