# AETHER Dockerfile
# Multi-stage build for minimal production image

# ─── Build Stage ───
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml setup.py README.md requirements.txt requirements-dev.txt ./
COPY aether/ ./aether/

# Build package
RUN pip install --no-cache-dir build && \
    python -m build --wheel --no-isolation

# ─── Runtime Stage ───
FROM python:3.12-slim AS runtime

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsqlite3-0 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r aether && useradd -r -g aether -d /app -s /bin/bash aether

# Copy built package from builder
COPY --from=builder /app/dist/*.whl /tmp/

# Install package
RUN pip install --no-cache-dir /tmp/*.whl && \
    rm /tmp/*.whl

# Create data directory
RUN mkdir -p /data/aether && chown -R aether:aether /data/aether

# Switch to non-root user
USER aether

# Environment
ENV AETHER_DATA_DIR=/data/aether
ENV PYTHONUNBUFFERED=1

# Entry point
ENTRYPOINT ["aether"]
CMD ["--help"]