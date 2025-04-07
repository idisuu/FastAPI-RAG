import os
import mimetypes

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.core.configs.config import main_config

common_router = APIRouter(
    tags=["Common"]
)

document_save_dir = main_config.DOCUMENT_SAVE_DIR

@common_router.get("/health-check")
def helath_check():
    return {"status": "healthy"}

@common_router.get("/{file_name}")
def downlaod_document(file_name: str):
    file_path = os.path.join(document_save_dir, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="파일이 존재하지 않습니다")

    # mimetypes를 이용해 파일의 MIME 타입을 추측
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "application/octet-stream"
    return FileResponse(path=file_path, filename=file_name, media_type=mime_type)