# Docker Deployment for Codebase Genius

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Jac
RUN pip install jaclang

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Create output directories
RUN mkdir -p outputs logs

# Expose port
EXPOSE 8000

# Start command
CMD ["jac", "serve", "main.jac"]
