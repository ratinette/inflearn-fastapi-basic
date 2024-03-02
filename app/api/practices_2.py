from fastapi import APIRouter, File, UploadFile, Form
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