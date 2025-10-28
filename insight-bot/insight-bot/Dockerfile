# Stage 1: Build stage with dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN pip install --upgrade pip

# Install requirements
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# ---

# Stage 2: Final production stage
FROM python:3.11-slim

WORKDIR /app

# Copy dependencies from builder stage
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY ./insight_bot ./insight_bot
COPY insight_bot.py .

# Create a non-root user for security
RUN useradd --create-home appuser
USER appuser

# Set the entrypoint
CMD ["python", "insight_bot.py"]