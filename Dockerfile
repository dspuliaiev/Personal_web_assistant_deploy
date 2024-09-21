# Stage 1: Build
FROM python:3.12-slim AS builder

# Set environment variables to prevent Python from writing .pyc files and to buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Update packages and install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip --no-cache-dir && pip install -r requirements.txt

# Copy the rest of the project code
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Stage 2: Final
FROM python:3.12-slim

# Set environment variables to prevent Python from writing .pyc files and to buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Update packages and install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev zlib1g \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local /usr/local

# Copy the rest of the project code
COPY . /app/

# Command to run Django using Gunicorn
CMD ["gunicorn", "--timeout", "120", "My_portfolio.wsgi:application", "--bind", "0.0.0.0:8000"]