from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found."}}
)

items_coll = {
    "item1": { "name": "item one" },
    "item2": { "name": "item two" },
}

@router.get("/")
async def read_items():
    return items_coll

@router.get("/{item_id}")
async def read_item(item_id: str):
    if (item_id not in items_coll):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")

    return {"name": items_coll[item_id]["name"], "item_id": item_id}

@router.put("/{item_id}", tags=["custom"], responses={403: {"description": "Operation forbidden."}})
async def update_item(item_id: str):
    if (item_id != "item1"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Updating this item is not allowed.")

    return {"item_id": item_id, "name": items_coll[item_id]["name"]}
