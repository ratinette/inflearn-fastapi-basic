import os
from typing import Literal

from fastapi import APIRouter, Header, Cookie, Form
from enum import Enum

from pydantic import EmailStr
from starlette.requests import Request
from starlette.responses import Response
from starlette.templating import Jinja2Templates


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
    if PythonFrameworkEnum.DJANGO == framework:
        return {"frameworks": "No Django"}
    return {"frameworks": framework}

LiteralFramework = Literal["django", "flask", "fastapi"]
@practice_router.get("/frameworks-literal")
async def get_frameworks_by_query_with_literal(framework: LiteralFramework):
    print(framework)
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


@practice_router.get("/header-test-ua", tags=["header&cookie"])
async def header_test(user_agent_2: str = Header(..., description="User-Agent")):
    return {"user_agent": user_agent_2}


@practice_router.get("/header-test-from-request", tags=["header&cookie"])
async def header_test_request(request: Request):
    user_agent = request.headers.get("user-agent")
    res = Response("User-Agent")
    res.headers["your-agent-1"] = user_agent
    return res


@practice_router.get("/cookie-test", tags=["header&cookie"])
async def cookie_test(session_token: str = Cookie(None)):
    return {"session_token": session_token}


@practice_router.get("/bake-cookie-test", tags=["header&cookie"])
async def cookie_set():
    res = Response("Cookie Set")
    res.set_cookie(
        key="session_token",
        value="fake-cookie",
        httponly=True,
        max_age=1800,
        expires=1800,
        path="/",
        domain="localhost"
    )
    return res


@practice_router.get("/cookie-test-from-request", tags=["header&cookie"])
async def cookie_test_request(request: Request):
    session_token = request.cookies.get("session_token")
    return {"session_token": session_token}


templates = Jinja2Templates(directory="templates")


@practice_router.get("/form-test", tags=["form"])
async def form_test(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@practice_router.post("/submit-form", tags=["form"])
async def submit_form_1(name: str = Form(...), email: EmailStr = Form(...)):
    print(name, email)
    return {"username": name, "password": email}


@practice_router.post("/submit-form-2", tags=["form"])
async def submit_form_2(request: Request, name: str = Form(...), email: EmailStr = Form(...)):
    return templates.TemplateResponse("form_result.html", {"request": request, "name": name, "email": email})