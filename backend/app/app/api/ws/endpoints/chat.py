from typing import List

from fastapi import FastAPI, WebSocket, APIRouter, Depends
from fastapi.websockets import WebSocketDisconnect

from app import models
from app.core.ws_manager import manager
from app.api import deps

router = APIRouter()

# prefix not working
# PR currently undergoing merge
@router.websocket("/api/live")
async def chat_room(
    ws: WebSocket,
    current_user: models.User = Depends(deps.get_authed_user_for_ws),
):
    user_email = current_user.email

    await manager.connect(ws)
    await manager.broadcast(f"User #{user_email} has entered the chat.")
    try:
        while True:
            data = await ws.receive_text()
            await manager.broadcast(f"User {user_email} say: {data}")
    except WebSocketDisconnect:
        manager.disconnect(ws)
        await manager.broadcast(f"User #{user_email} has left the chat.")
