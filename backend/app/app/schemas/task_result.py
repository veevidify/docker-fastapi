from celery.result import ResultBase

class TaskResult(ResultBase):
    ordered_by: str
