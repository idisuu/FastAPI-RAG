from fastapi import APIRouter, Depends

from app.core.services.generate_service import get_generate_service

generate_router = APIRouter(
    tags=["Generate"]
)

@generate_router.post("/generate")
def generate(query: str, generate_service=Depends(get_generate_service)):    
    result = generate_service.generate(query)
    return result