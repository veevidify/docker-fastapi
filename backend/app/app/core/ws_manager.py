from typing import List

from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketDisconnect

class ConnManager:
    def __init__(self):
        self.active_ws_conns: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_ws_conns.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active_ws_conns.remove(ws)

    async def send_msg(self, msg: str, ws: WebSocket):
        await ws.send_text(msg)

    async def broadcast(self, msg: str):
        # send sequentially
        for conn in self.active_ws_conns:
            await conn.send_text(msg)

manager = ConnManager()
