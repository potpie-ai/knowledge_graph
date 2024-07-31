#!/bin/bash
source .env

# Start celery worker and main application
echo "Starting Celery worker..."
celery --app=inferflow worker -l INFO --pool solo -Q ${CELERY_QUEUE_NAME} &

echo "Starting main application..."
python3 main.py &