from enum import Enum
from typing import Optional
from pydantic import BaseModel

from fastapi import FastAPI, Query, Path, Body, Cookie, Header, Depends, HTTPException

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Beginning of the app"}

# basic
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "current_user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# enum
class ModelName(str, Enum):
    oc_svm = "ocsvm"
    iforest = "iforest"
    abod = "abod"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    return {"model": model_name}

# public file as param
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# indexing array of dicts
items = [{"item_name": "first item"}, {"item_name": "second item"}, {"item_name": "third item"}]

@app.get("/items/")
async def read_item(skip: int=0, limit: int=10):
    return items[skip: skip + limit]

# parameterized
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
    if (q):
        return {"item_id": item_id, "q" : q}
    else:
        return {"item_id": item_id}

# post body
class Item(BaseModel):
    name: str
    desc: Optional[str] = None
    price: float

@app.post("/items/", status_code=201)
async def create_item(item: Item):
    return item

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

# query validation
@app.get("/read-items/")
async def read_multiple_items(
    q: Optional[str] = Query(
        None,
        min_length=3,
        max_length=50,
        regex="^fixedprefix"
    )
):
    results = {"items": items}
    if q:
        results.update({"q": q})

    return results

@app.get("/read-items-list")
async def read_items_list(q: list = Query(..., alias="q")):
    q_items = {"items": items}
    q_items.update({"q": q})

    return q_items

# path validation
@app.get("/read-items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="ID of item", ge=1),
    q: Optional[str] = Query(None, alias="q"),
):
    results = {"item_id": item_id}
    if (q):
        results.update({"q": q})

    return results

# body param (typed, multiple)
@app.put("/put-items/{item_id}")
async def put_items(
    item_id: int = Path(..., title="ID of items", ge=1),
    q: Optional[str] = None,
    item: Optional[Item] = Body(
        ...,
        embed=True
    )
):
    results = {"item_id": item_id}
    if (q):
        results.update({"q": q})
    if (item):
        results.update({"item": item})

    return results

@app.put("/update-items/{item_id}")
async def update_items(
    item_id: int = Path(..., title="ID of items", ge=1),
    q: Optional[str] = None,
    item: Optional[Item] = Body(
        ...,
        example={
            "name": "a",
            "desc": "b",
            "price": 3.14
        }
    )
):
    results = {"item_id": item_id}
    if (q):
        results.update({"q": q})
    if (item):
        results.update({"item": item})

    return results

# cookie
@app.get("/retrieve-items/")
async def retrieve_items(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}

# header
@app.get("/ping1")
async def ping1(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}

@app.get("/ping2")
async def ping2(strange_header: Optional[str] = Header(None, convert_underscores=False)):
    return {"strange_header": strange_header}

# typed response
@app.post("/item/", response_model=Item, status_code=201)
async def post_item(item: Item):
    return item

# merging types by unwrapping
class ItemReq(BaseModel):
    name: Optional[str]
    desc: Optional[str]

class ItemRes(BaseModel):
    name: str
    desc: str

@app.post("/update-item", response_model=ItemRes, status_code=201)
async def update_item(item: ItemReq = Body(..., embed=True)):
    existing_item = {
        "name": "a",
        "desc": "b",
    }
    item_merge = existing_item
    for k, v in item.dict().items():
        if (v):
            item_merge[k] = v

    return ItemRes(**item_merge)

# dependencies for verification
# for global usage:
# app = FastAPI(dependencies=[Depends(verify_token)])
async def verify_token(x_token: str = Header(...)):
    if (x_token != "my-secret-token"):
        raise HTTPException(status_code=400, detail="X-Token header invalid")

@app.get("/verified-items/", dependencies=[Depends(verify_token)])
async def verified_items():
    return items
