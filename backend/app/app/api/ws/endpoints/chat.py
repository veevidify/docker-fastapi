from typing import List

from fastapi import FastAPI, WebSocket, APIRouter, Depends
from fastapi.websockets import WebSocketDisconnect

from app import models
from app.core.ws_manager import manager
from app.api import deps

router = APIRouter()

# prefix not working
# PR currently undergoing merge
@router.websocket("/api/live/{client_id}")
async def chat_room(
    ws: WebSocket,
    client_id: int,
    current_user: models.User = Depends(deps.get_authed_user_for_ws),
):
    await manager.connect(ws)
    await manager.broadcast(f"Client #{client_id} has entered the chat.")
    try:
        while True:
            data = await ws.receive_text()
            await manager.broadcast(f"Client #{client_id} say: {data}")
    except WebSocketDisconnect:
        manager.disconnect(ws)
        await manager.broadcast(f"Client #{client_id} has left the chat.")
