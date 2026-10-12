# Multi-stage Dockerfile for EYAN AI (عِيَان)
# Builds Frontend and serves unified full-stack with FastAPI & Face Recognition

# Stage 1: Build React Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Python Backend with OpenCV & Headless Chromium
FROM python:3.11-slim
WORKDIR /app

# Install system libraries for OpenCV headless and Chromium for PDF rendering
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    chromium \
    fonts-noto \
    fonts-noto-color-emoji \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN=/usr/bin/chromium

# Install Python requirements
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend app & assets
COPY backend/ ./backend/

# Copy built frontend from Stage 1
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

WORKDIR /app/backend

# Environment variables
ENV PORT=8000
ENV PYTHONUNBUFFERED=1
EXPOSE 8000

# Start command
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
