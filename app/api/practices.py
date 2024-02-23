import os

from fastapi import APIRouter
from enum import Enum


class PythonFrameworkEnum(str, Enum):
    DJANGO = "django"
    FLASK = "flask"
    FASTAPI = "fastapi"


practice_router = APIRouter()


@practice_router.get("/sum")
async def sum_calc(int1: int, int2: int):
    return {"result": int1 + int2}


@practice_router.get("/sum_str")
async def sum_calc_w_str(int1: str, int2: str):
    return {"result": int1 + int2}


@practice_router.get("/frameworks")
async def get_frameworks_by_query(framework: PythonFrameworkEnum):
    return {"frameworks": framework}


@practice_router.get("/frameworks-literal")
async def get_frameworks_by_query_with_literal(framework: Literal["django", "flask", "fastapi"]):
    return {"frameworks": framework}


@practice_router.get("/frameworks/{framework}")
async def get_frameworks(framework: PythonFrameworkEnum):
    return {"frameworks": framework}


@practice_router.get("/files/{file_path:path}")
async def get_file(file_path: str):
    os_path = os.path.join(os.getcwd(), "app/api", file_path)
    if not os.path.exists(os_path):
        return {"file_path": "File Not Found"}
    with open(os_path, "r") as file:
        content = file.read()
    return content
