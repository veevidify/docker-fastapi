from raven import Client

from celery.utils.log import get_task_logger

from app.core.celery_app import celery_app
from app.core.config import settings

client_sentry = Client(settings.SENTRY_DSN)

celery_log = get_task_logger(__name__)

@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    celery_log.info(f"Task completed.")
    return f"test task return {word}"
