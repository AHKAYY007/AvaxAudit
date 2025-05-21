FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY linux-requirements.txt .
RUN pip install --no-cache-dir -r linux-requirements.txt

# Copy application code
COPY . .

# Fix alembic.ini - ensure script_location is set correctly
RUN sed -i '/^\[alembic\]/,/^\[/ s/^#*script_location.*/script_location = alembic/' alembic.ini && \
    grep -q "script_location = alembic" alembic.ini || echo "script_location = alembic" >> alembic.ini

# Expose port
EXPOSE 8000

# Command to run migrations and start the application
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
