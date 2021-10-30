from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from celery.result import ResultBase
import logging

from app import schemas, models
from app.api import deps
from app.worker import test_celery

router = APIRouter()
log = logging.getLogger(__name__)

# these are available for different backend than the one configured
# e.g. redis instead of amqp

# def celery_on_message(message):
#     log.warn(message)

# def background_on_message(task):
#     log.warn(task.get(on_message=celery_on_message, propagate=False))

@router.get("/order-celery")
def send_task_to_celery(
    # background_task: BackgroundTasks,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    q: Optional[str] = Query(None, alias="q"),
):
    """
    example to send task to celery worker
    """
    word = "not specified"
    if (q is not None):
        word = q

    task = test_celery.delay(word)
    print(task)
    # try alternative backend (redis instead of amqp) to collect callback
    # background_task.add_task(background_on_message, task)

    return {"message": "Task ordered"}
