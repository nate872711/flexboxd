# ============================================================
# 🐳 WatchWeave - Unified Media Sync Service
# ============================================================

FROM python:3.12-slim AS base

# Prevent Python from writing .pyc files and buffer logs
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# ------------------------------------------------------------
# Install dependencies
# ------------------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ------------------------------------------------------------
# Copy application files
# ------------------------------------------------------------
COPY src/ ./src/
COPY scripts/ ./scripts/

# Ensure /config and /logs directories exist
RUN mkdir -p /config /logs

# ------------------------------------------------------------
# Entrypoint Script
# ------------------------------------------------------------
# The entrypoint runs a tiny bootstrap to:
#   1. Check if /config/config.yml exists
#   2. Auto-generate it from environment variables if missing
#   3. Start the WatchWeave service

RUN echo '#!/usr/bin/env bash\n' \
    'set -e\n' \
    'if [ ! -f "/config/config.yml" ]; then\n' \
    '  echo "🧩 No config.yml found — generating from environment variables..."\n' \
    '  python -c "from src.config_loader import generate_config_from_env; generate_config_from_env()"\n' \
    '  echo "✅ Config file created at /config/config.yml"\n' \
    'else\n' \
    '  echo "✅ Using existing config.yml"\n' \
    'fi\n' \
    'echo "🚀 Starting WatchWeave..."\n' \
    'exec python -m src.main\n' \
    > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# ------------------------------------------------------------
# Expose the web UI port
# ------------------------------------------------------------
EXPOSE 8089

# ------------------------------------------------------------
# Metadata
# ------------------------------------------------------------
LABEL org.opencontainers.image.title="WatchWeave" \
      org.opencontainers.image.description="Media sync tool for Plex, Trakt, Letterboxd, and IMDb" \
      org.opencontainers.image.source="https://github.com/nate872711/watchweave" \
      org.opencontainers.image.licenses="MIT"
