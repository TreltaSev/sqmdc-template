# === Core ===
from fastapi import APIRouter, Response

router = APIRouter()

@router.get("/health")
async def auth(response: Response):
    response.status_code = 200
    return response