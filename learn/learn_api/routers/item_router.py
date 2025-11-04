from fastapi import APIRouter
from models import Item

router = APIRouter(prefix="/api")

@router.post("/items")
async def create_item(item: Item):
    return {"received": item.dict()}