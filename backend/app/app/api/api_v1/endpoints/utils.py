from typing import Any

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr
from celery.result import AsyncResult

from app import models, schemas
from app.api import deps
from app.worker import celery_app
from app.utils import send_test_email

router = APIRouter()


@router.post("/queue-celery-task/", response_model=schemas.ResponseMsg, status_code=201)
def test_celery(
    msg: schemas.Msg,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    handle: AsyncResult = celery_app.send_task("app.worker.run_task", args=[msg.msg])
    return {"msg": "Word received", "task_id": handle.task_id}

@router.get("/task-status/{task_id}", response_model=schemas.TaskStatus)
def task_status(
    task_id: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """query celery task status"""
    task_result = AsyncResult(task_id, app=celery_app)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return result

@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
