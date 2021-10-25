from fastapi import FastAPI, Header, HTTPException, status
from fastapi.testclient import TestClient

from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def main():
    return {"message": "Hello"}

# some configs
mock_token = "secrettoken"
coll = {
    "item1": {
        "id": "1",
        "title": "item one",
        "desc": "item"
    },
    "item2": {
        "id": "2",
        "title": "item two",
        "desc": "item"
    },
}

class Item(BaseModel):
    id: str
    title: str
    desc: Optional[str] = None

@app.get("/items/{item_id}", response_model=Item)
async def main(item_id: str, x_token: str = Header(...)):
    if (x_token != mock_token):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid X-Token header.")
    if (item_id not in coll):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")

    return coll[item_id]

@app.post("/items/", response_model=Item)
async def create_item(item: Item, x_token: str = Header(...)):
    if (x_token != mock_token):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid X-Token header.")
    if (item.id in coll):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item exists.")

    coll[item.id] = item
    return item
