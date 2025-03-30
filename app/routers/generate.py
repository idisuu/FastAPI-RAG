from fastapi import APIRouter, Depends

from app.core.services.generate_service import get_generate_service
from app.db.chroma_db import get_vectordb

generate_router = APIRouter(
    tags=["Generate"]
)

@generate_router.post("/generate")
def generate(query: str, use_rag: bool, generate_service=Depends(get_generate_service), vectordb=Depends(get_vectordb)):    
    result = generate_service.generate(query=query, use_rag=use_rag, vectordb=vectordb)
    return result