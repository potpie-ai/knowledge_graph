#!/bin/bash
celery --app=inferflow worker -l INFO --pool solo -Q ${CELERY_QUEUE_NAME}