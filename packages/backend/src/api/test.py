from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
async def read_test():
    return {"ok": True}