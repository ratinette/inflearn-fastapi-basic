from typing import Optional

from fastapi import APIRouter, File, UploadFile, Form
from pydantic import BaseModel, create_model
from starlette.requests import Request
from starlette.templating import Jinja2Templates

practice_router2 = APIRouter()
templates = Jinja2Templates(directory="templates")

@practice_router2.post("/files")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@practice_router2.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    allowed_file_types = ["image/jpeg", "image/png", "image.gif"]
    if file.content_type not in allowed_file_types:
        return {"error": f"File Type Not Allowed. current type: {file.content_type}"}
    return {"filename": file.filename}


@practice_router2.post("/uploadfiles")
async def upload_multi_files(files: list[UploadFile] = File(...)):
    for file in files:
        print(file.filename)
    return {"count": len(files)}



@practice_router2.get("/form_upload")
async def form_upload(request: Request):
    return templates.TemplateResponse("form_with_file.html", {"request": request})


@practice_router2.post("/form_upload")
async def form_upload_file(name: str = Form(...), email: str = Form(...), file: UploadFile = File(...)):
    return {"name": name, "email": email, "filename": file.filename}


class User(BaseModel):
    name: str
    age: Optional[int] = None


@practice_router2.post("/user/update/")
async def update_user(user_json: str):
    try:
        # JSON 문자열을 Pydantic 모델로 변환
        user = User.model_validate(user_json)
        # 모델 인스턴스의 깊은 복사본 생성
        original_user = user.model_copy()
    except Exception as e:
        return {"error": f"Invalid JSON: {str(e)}"}

    # 데이터 수정 (예시: 나이를 업데이트)
    user.age = (user.age or 0) + 1

    # 수정된 모델과 원본 모델을 JSON으로 변환하여 반환
    return {
        "updated_user": user.model_dump_json(),
        "original_user": original_user.model_dump_json()
    }


class UserProfile(BaseModel):
    username: str
    profile: Optional["UserProfile"] = None


UserProfile.model_rebuild()


@practice_router2.put("/user/profile/{username}")
async def update_user_profile(username: str):
    # 검증 없이 직접적으로 모델 인스턴스 생성
    user_profile = UserProfile.model_construct()
    # user_profile = create_model("UserProfile", username=(str, ...), profile=(Optional[UserProfile], None))()
    user_profile.username = username
    user_profile.profile = UserProfile(username=username + "_profile")

    return user_profile.model_dump()
