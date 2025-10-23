# Docker Deployment for Codebase Genius

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Jac
RUN pip install jaclang

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy codebase_genius directory
COPY codebase_genius ./codebase_genius

# Copy sample repository for testing
COPY sample_repo ./sample_repo

# Create output directories
RUN mkdir -p outputs logs

# Set working directory to where main.jac is located
WORKDIR /app/codebase_genius

# Expose port
EXPOSE 8000

# Start command
CMD ["jac", "serve", "main.jac"]
