from fastapi import APIRouter


practice_router = APIRouter()


@practice_router.get("/")
async def root():
    return {"message": "Hello World"}
