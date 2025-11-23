# Multi-stage build for N7M MCP Server
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml README.md LICENSE ./
COPY src ./src

# Install dependencies and build
RUN uv pip install --system --no-cache .

# Runtime stage
FROM python:3.12-slim

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 n7m && \
    mkdir -p /app && \
    chown -R n7m:n7m /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application
WORKDIR /app
COPY --chown=n7m:n7m src ./src

# Switch to non-root user
USER n7m

# Set Python path
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import n7m; print(n7m.__version__)" || exit 1

# Default to stdio transport
ENTRYPOINT ["python", "-m", "n7m.server"]
CMD ["--transport", "stdio"]

# Labels
LABEL org.opencontainers.image.title="N7M MCP Server"
LABEL org.opencontainers.image.description="Nominatim geocoding service via Model Context Protocol"
LABEL org.opencontainers.image.version="0.1.0"
LABEL org.opencontainers.image.authors="Jonathan Springer <jps@s390x.com>"
LABEL org.opencontainers.image.source="https://github.com/jonpspri/n7m-mcp"
LABEL org.opencontainers.image.licenses="Apache-2.0"
