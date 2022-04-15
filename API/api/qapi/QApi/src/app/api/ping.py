from typing import Optional
from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/ping")
async def pong():
    # some async operation could happen here
    # example: `notes = await get_all_notes()`

    return {"ping": "pong!"}

@router.get("/path")
def read_main(request: Request):
    return {"message": "Path", "root_path": request.scope.get("root_path")}


@router.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
    