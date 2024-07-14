# Use the official Python base image
FROM python:3.12-bullseye

# Expose the necessary ports
EXPOSE 8000
EXPOSE 8080
EXPOSE 5432
EXPOSE 80
EXPOSE 5050

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=123456
ENV POSTGRES_DB=postgres

# Create PostgreSQL data directory
RUN mkdir -p /var/lib/postgresql/data