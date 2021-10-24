from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware

import time

app = FastAPI()

allowed_origins = [
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "OPTIONS", "PATCH", "DELETE"],
    allow_headers=["*"]
)

@app.middleware("http")
async def process_time_header(request: Request, next):
    start = time.time()
    resp = await next(request)
    time_lapsed = time.time() - start
    resp.headers["X-Process-Time"] = str(time_lapsed)

    return resp

@app.get("/hello")
async def root():
    return "Hello"
