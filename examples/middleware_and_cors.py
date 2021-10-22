from fastapi import FastAPI, Depends, HTTPException, status, Request

import time

app = FastAPI()

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
