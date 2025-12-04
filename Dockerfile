# ============================================================
# EditalShield - Dockerfile
# Multi-stage build for production-ready container
# ============================================================

FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# ============================================================
# Production Stage
# ============================================================
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash editalshield
USER editalshield

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install dependencies
RUN pip install --no-cache --user /wheels/*

# Copy application code
COPY --chown=editalshield:editalshield . .

# Set PATH for user-installed packages
ENV PATH="/home/editalshield/.local/bin:$PATH"
ENV PYTHONPATH="/app/src:$PYTHONPATH"
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from database.models import SessionLocal; db = SessionLocal(); db.execute('SELECT 1'); print('OK')" || exit 1

# Default command
CMD ["python", "-m", "editalshield", "--help"]
