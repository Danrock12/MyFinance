from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_transactions():
    return [{"id": 1, "name": "Sample Transaction"}]
