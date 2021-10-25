from fastapi import FastAPI, Depends, status

from .dependencies import get_query_token, get_token_header
from .admin import admin
from .routing import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}}
)

@app.get("/")
async def root():
    return {"message": "hello"}
