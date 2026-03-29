# Use an official Python runtime as a parent image
FROM python:3.10-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install LibreOffice and required system dependencies
# Installing fonts is recommended for better document conversion quality
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice \
    libreoffice-writer \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of the project code
COPY . /app/

# Create media and static directories, and ensure tmp conversion directory exists
RUN mkdir -p /app/upload_files /app/static /tmp/converted_files && \
    chmod 777 /tmp/converted_files

# Commands are handled via docker-compose
