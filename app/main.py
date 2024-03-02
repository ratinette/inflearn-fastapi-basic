import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger

from app.api import practice_router
from app.api.practices_2 import practice_router2


def app():
    fastapi_app = FastAPI()
    # DB Connection

    # Add Middlewares

    # Add Routers
    fastapi_app.include_router(practice_router, prefix="/practices", tags=["PRACTICES"])
    fastapi_app.include_router(practice_router2, prefix="/practices2", tags=["PRACTICES2"])

    @fastapi_app.on_event("startup")
    def startup_event():
        logger.info("Server Startup")

    @fastapi_app.on_event("shutdown")
    def shutdown_event():
        logger.info("Server Shutdown")

    return fastapi_app


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, factory=True)
