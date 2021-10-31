from pydantic import BaseModel

class TaskStatus(BaseModel):
    task_id: str
    task_status: str
    task_result: str
