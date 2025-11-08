# ──────────────────────────────────────────────
#   WatchWeave Dockerfile
#   Maintained for Python 3.11+
# ──────────────────────────────────────────────

FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create application directory
WORKDIR /app

# ──────────────────────────────────────────────
#   Install required system dependencies
# ──────────────────────────────────────────────
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        wget \
        tzdata \
        && rm -rf /var/lib/apt/lists/*

# ──────────────────────────────────────────────
#   Copy application files
# ──────────────────────────────────────────────
COPY src/ /app/src/
COPY requirements.txt /app/

# ──────────────────────────────────────────────
#   Install Python dependencies
# ──────────────────────────────────────────────
# Make sure PyYAML and other core libraries are present
RUN pip install --no-cache-dir -r requirements.txt || \
    pip install --no-cache-dir pyyaml requests python-dotenv rich

# ──────────────────────────────────────────────
#   Create config and log directories
# ──────────────────────────────────────────────
RUN mkdir -p /config /logs

# ──────────────────────────────────────────────
#   Set timezone environment variable (overridable)
# ──────────────────────────────────────────────
ENV TZ=Etc/UTC

# ──────────────────────────────────────────────
#   Expose default internal port
# ──────────────────────────────────────────────
EXPOSE 8089

# ──────────────────────────────────────────────
#   Define entrypoint
# ──────────────────────────────────────────────
CMD ["python", "-u", "/app/src/main.py"]
