from typing import Optional
from pydantic import BaseModel


class Msg(BaseModel):
    msg: str

class ResponseMsg(Msg):
    task_id: str

class WSResponse(BaseModel):
    scope: str
    intent: str
    by: str
    message: str
