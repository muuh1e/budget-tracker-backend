#!/bin/bash

echo "Starting entrypoint script..."

# --- ADD THESE TWO LINES AT THE VERY BEGINNING ---
# Ensure the /app directory (including mounted volume contents) is owned by appuser
# This is crucial when host user IDs don't match container user IDs.
chown -R appuser:appuser /app
chmod -R u+rwX /app # Ensure appuser has read/write/execute on app directory contents
# -------------------------------------------------

# Existing wait-for-db and wait-for-redis logic
echo "Waiting for PostgreSQL to be ready on db:5432..."
timeout 30 bash -c 'until echo > /dev/tcp/db/5432; do sleep 0.5; done'
if [ $? -ne 0 ]; then
  echo "PostgreSQL did not become ready in time!"
  exit 1
fi
echo "PostgreSQL is up and running!"

echo "Waiting for Redis to be ready on redis:6379..."
timeout 30 bash -c 'until echo > /dev/tcp/redis/6379; do sleep 0.5; done'
if [ $? -ne 0 ]; then
  echo "Redis did not become ready in time!"
  exit 1
fi
echo "Redis is up and running!"

# Check if the command is 'python manage.py runserver'
if [[ "$@" == "python manage.py runserver 0.0.0.0:8000" ]]; then
  echo "Applying database migrations (if not already applied)..."
  python manage.py migrate --noinput
  echo "Executing: $@"
  exec "$@"
# Check if the command is 'celery' or 'celery -A ...'
elif [[ "$@" == celery* ]]; then
  echo "Executing: $@"
  exec "$@"
else
  # Default command if nothing specific is matched
  echo "Executing: $@"
  exec "$@"
fi
