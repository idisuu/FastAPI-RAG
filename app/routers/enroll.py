from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import PlainTextResponse

from app.core.services.enroll_service import get_enroll_service

from app.db.chroma_db import get_vectordb

from app.core.utils.logger import logger

enroll_router = APIRouter(
     tags=["Enroll"]
)


@enroll_router.post("/enroll/file")
async def enroll_file(file: UploadFile, enroll_service=Depends(get_enroll_service), vectordb=Depends(get_vectordb)):
    content = await file.read()
    extension = file.filename.split(".")[-1]
    
    enroll_service.enroll(content=content, vectordb=vectordb, file_name=file.filename, extension=extension)
            
    return {"status": "success"}

@enroll_router.get("/enroll/registered-files", response_class=PlainTextResponse)
def get_registered_files(
    enroll_service=Depends(get_enroll_service),
    vectordb=Depends(get_vectordb)
):
    """
    등록된 모든 파일 목록을 텍스트 파일 형태로 반환하는 엔드포인트.
    """
    text_content = enroll_service.get_registered_files(vectordb)
    headers = {
        "Content-Disposition": 'attachment; filename="registered_files.txt"'
    }
    return PlainTextResponse(text_content, headers=headers)