from fastapi import FastAPI, Depends

from functools import lru_cache

from .config import Settings

app = FastAPI()

# turn configs to dependency - override-able
@lru_cache()
def get_settings():
    return Settings()

@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "app_key": settings.app_key
    }
