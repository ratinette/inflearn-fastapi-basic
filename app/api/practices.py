from fastapi import APIRouter


practice_router = APIRouter()


@practice_router.get("/sum")
async def sum(int1: int, int2: int):
    return {"sum": int1 + int2}
