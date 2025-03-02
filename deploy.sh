#!/bin/bash

# Update dependencies
pip install -r requirements.txt

# Run database migrations
python -m alembic upgrade head

# Start services
docker-compose up --build -d

# Run tests
pytest tests/

# Optional: Cleanup
docker-compose logs