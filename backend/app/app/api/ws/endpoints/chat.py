import json
from typing import List

from fastapi import FastAPI, WebSocket, APIRouter, Depends
from fastapi.websockets import WebSocketDisconnect
from fastapi.encoders import jsonable_encoder

from app import models
from app import schemas
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
    payload = schemas.WSResponse(
        scope="chat",
        intent="connection_status",
        by=user_email,
        message=f"User #{user_email} has entered the chat.",
    )
    resp_json = jsonable_encoder(payload)
    await manager.broadcast(json.dumps(resp_json))

    try:
        while True:
            data = await ws.receive_text()
            payload = schemas.WSResponse(
                scope="chat",
                intent="user_message",
                by=user_email,
                message=data,
            )
            resp_json = jsonable_encoder(payload)
            await manager.broadcast(json.dumps(resp_json))

    except WebSocketDisconnect:
        manager.disconnect(ws)
        payload = schemas.WSResponse(
            scope="chat",
            intent="connection_status",
            by=user_email,
            message=f"User #{user_email} has left the chat.",
        )
        resp_json = jsonable_encoder(payload)
        await manager.broadcast(json.dumps(resp_json))
