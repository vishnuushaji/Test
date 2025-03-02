#!/bin/bash

# Wait for database to be ready
until nc -z -v -w30 db 3306
do
  echo "Waiting for database connection..."
  sleep 5
done

# Run database migrations
alembic upgrade head

# Start the application
exec "$@"