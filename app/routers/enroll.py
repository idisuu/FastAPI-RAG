from fastapi import APIRouter, UploadFile, Depends

from app.core.services.enroll_service import enroll_service

from app.db.chroma_db import get_vectordb

from app.core.utils.logger import logger

enroll_router = APIRouter(
     tags=["Enroll"]
)


@enroll_router.post("/enroll/file")
async def enroll_file(file: UploadFile, vectordb=Depends(get_vectordb)):
    content = await file.read()
    extension = file.filename.split(".")[-1]
    
    enroll_service.enroll(content=content, vectordb=vectordb, file_name=file.filename, extension=extension)
            
    return {"status": "success"}