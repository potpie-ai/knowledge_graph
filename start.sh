# Start celery worker and main application
echo "Starting Celery worker..."
celery --app=inferflow worker -l INFO --pool solo -Q dev &

echo "Starting main application..."
python3 main.py &