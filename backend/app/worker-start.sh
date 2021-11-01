#! /usr/bin/env bash
set -e

python /app/app/celeryworker_pre_start.py

celery worker --app=app.worker.celery_app -l info -Q main-queue -c 1
