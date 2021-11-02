from fastapi import APIRouter

from app.api.ws.endpoints import chat

ws_router = APIRouter()

# prefix not working,
# PR currently undergoing merge
ws_router.include_router(chat.router, tags=["chat"])
