python3 main.py

celery --app=inferflow worker -l INFO --concurrency=5 --pool solo