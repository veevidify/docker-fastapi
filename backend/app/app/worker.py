import os

from celery import Celery
from celery.utils.log import get_task_logger
from raven import Client

from app.core.config import settings

celery_app = Celery(__name__)

# configs
celery_app.conf.broker_url = os.getenv("BROKER_URL", "redis://localhost:6379/0")
celery_app.conf.backend = os.getenv("RESULT_BACKEND", "redis://localhost:6379/0")
celery_app.conf.task_routes = {"app.worker.test_celery": "main-queue"}
client_sentry = Client(settings.SENTRY_DSN)

celery_log = get_task_logger(__name__)

@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    celery_log.info(f"Task completed.")
    return f"test task return {word}"
