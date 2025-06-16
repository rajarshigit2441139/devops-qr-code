# Stage 1: Builder
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /usr/src/app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into a virtual environment
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Final image
FROM python:3.11-slim

# Set working directory
WORKDIR /usr/src/app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy app source code
COPY . .

# Use virtualenv binaries
ENV PATH="/opt/venv/bin:$PATH"

# Expose application port
EXPOSE 80

# Run app with hot reload (used only in development, consider removing in production)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
