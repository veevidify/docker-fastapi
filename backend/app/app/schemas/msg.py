from typing import Optional
from pydantic import BaseModel


class Msg(BaseModel):
    msg: str

class ResponseMsg(Msg):
    task_id: str
