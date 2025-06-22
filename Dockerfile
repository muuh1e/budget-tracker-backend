# Use the official Python image from the Docker Hub as the base image
FROM python:3.12.4-slim

# Install system dependencies for Postgres, building wheels, and networking
# Keep only necessary packages to reduce image size
# netcat-openbsd is for waiting for services in entrypoint.sh
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev netcat-openbsd \
    wget \
    && rm -rf /var/lib/apt/lists/*
# Create app directory
WORKDIR /app

# --- START OF MODIFIED SECTION FOR USER/GROUP ---
# Define build arguments for UID/GID
ARG HOST_UID
ARG HOST_GID

# Create a non-root group with specified GID (if it doesn't exist, ignore error with || true)
RUN groupadd -g ${HOST_GID} appuser || true

# Create a non-root user with specified UID and add to the group
# Using --system and --no-create-home for a cleaner system user
RUN useradd -u ${HOST_UID} -g appuser --system --no-create-home appuser
# --- END OF MODIFIED SECTION ---

# Copy project requirements and install Python dependencies
# These RUN commands are still performed as root, which is fine.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose port 8000 for the Django development server
EXPOSE 8000

# Define the entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch to the non-root user for subsequent commands and at runtime
USER appuser

# Use ENTRYPOINT to always run our custom script
# And CMD for the default command that ENTRYPOINT script will execute
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]