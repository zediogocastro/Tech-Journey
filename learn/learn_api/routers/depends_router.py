from fastapi import APIRouter, Depends
from deps import FakeDBClient, get_client

router = APIRouter(prefix="/api/v1")

@router.get("/price")
async def get_price(name: str, client: FakeDBClient = Depends(get_client)):
    return {"name": name, "price": client.get_price(name)}