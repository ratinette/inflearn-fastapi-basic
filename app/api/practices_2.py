import copy
from typing import Optional

from fastapi import APIRouter, File, UploadFile, Form, Body
from pydantic import BaseModel, create_model, field_validator, model_validator
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
        user = User.model_validate_json(user_json)
        # 모델 인스턴스의 깊은 복사본 생성
        original_user = user.model_copy()
    except Exception as e:
        return {"error": f"Invalid JSON: {str(e)}"}

    # 데이터 수정 (예시: 나이를 업데이트)
    user.age = (user.age or 0) + 1

    # 수정된 모델과 원본 모델을 JSON으로 변환하여 반환
    return {
        "updated_user": user.model_dump(),
        "original_user": original_user.model_dump()
    }


class UserProfile(BaseModel):
    username: str
    email: Optional[str] = None
    age: int
    profile: Optional["AuxProfile"] = None

    @field_validator("username", mode="after")
    def check_username(cls, v):
        if len(v) < 3:
            raise ValueError("username must be more than 3 characters")
        return v

    @field_validator("email", mode="wrap")
    def check_email(cls, v, validator):
        print("검사전 :", v)
        email = copy.deepcopy(v)
        if not v:
            email = "example@test.com"
        email = validator(email)
        print("검사후 :", email)
        return email

    @model_validator(mode="after")
    def check_profile(self):
        if self.age < 18 and self.email.endswith("test.com"):
            raise ValueError("No @test.com domain with age under 18")

        return self


class AuxProfile(BaseModel):
    more_info: str = "No Info"


class ResponseModel(BaseModel):
    ok: bool
    status: int = 200


@practice_router2.post("/user/profile/{username}")
async def create_user_profile(username: str, age: int, email: Optional[str] = None):
    # 검증 없이 직접적으로 모델 인스턴스 생성
    user_profile = UserProfile.model_construct()
    user_profile.username = username
    user_profile.age = age
    user_profile.email = email
    user_profile.profile = AuxProfile()

    return user_profile.model_dump()

class ErrorResponse(BaseModel):
    status_code: int
    message: str

@practice_router2.post(
    "/user/profile2",
    response_model=ResponseModel,
    status_code=201,
    summary="유저 프로필을 생성하는 엔드포인트 입니다.",
    response_description="유저 프로필 생성 성공",
    responses={201:{"model":ResponseModel}, 400:{"model":ErrorResponse}, 500:{"model":ErrorResponse}},
    operation_id="create_user_profile_2",
    include_in_schema=True,
    deprecated=False,
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "required": ["name", "price"],
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "price": {"type": "number"},
                            "description": {"type": "string"},
                        },
                    }
                }
            },
            "required": True,
        },
    },
)
async def create_user_profile_2(profile: UserProfile = Body()):
    """
    - `username(*)`, `email`, `age(*)`, `profile`, 이메일의 경우 빈 값으로 입력될 경우 test@test.com으로 변경됨
      - `(*)` 필수
    - `email`이 @test.com 도메인을 사용하면서 18세 미만은 등록 불가
    """
    return {"ok": True}


class Foo(BaseModel):
    value: "LazyValue"

class Bar(BaseModel):
    a: Foo


@practice_router2.post("/user/model_rebuild")
async def model_rebuild():
    model()
    bar = Bar(a={"value": {"b": "test"}})
    print(bar.model_dump())
    return None


def model():
    class LazyValue(BaseModel):
        b: str
    Bar.model_rebuild()
    return LazyValue







