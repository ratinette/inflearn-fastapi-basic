import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.staticfiles import StaticFiles

from app.api import practice_router
from app.api.practices_2 import practice_router2

APP_NAME = "My Quiz API"
APP_VERSION = "1.0.1"
APP_DESC = """
- `FastAPI` 강좌용 API 서버입니다.
- `FastAPI`를 활용하여 API 서버를 구축하는 방법을 학습합니다.
- `FastAPI`를 활용하여 API 서버를 구축하는 방법을 학습합니다.

![FastAPI](https://picsum.photos/800/300)
"""

def app():
    fastapi_app = FastAPI()

    fastapi_app.mount("/static", StaticFiles(directory="static"), name="static")

    @fastapi_app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=fastapi_app.openapi_url,
            title=fastapi_app.title + " - Swagger UI!!!",
            swagger_css_url="/static/theme-flattop.css",
        )

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

    def custom_openapi():
        if fastapi_app.openapi_schema:
            return fastapi_app.openapi_schema
        openapi_schema = get_openapi(
            title=APP_NAME,
            version=APP_VERSION,
            summary="안녕하세요.",
            description=APP_DESC,
            routes=fastapi_app.routes,
        )
        fastapi_app.openapi_schema = openapi_schema
        return fastapi_app.openapi_schema

    fastapi_app.openapi = custom_openapi

    return fastapi_app


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, factory=True)
