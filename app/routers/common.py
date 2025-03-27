from fastapi import APIRouter

common_router = APIRouter(
    tags=["Common"]
)

@common_router.get("/health-check")
def helath_check():
    return {"status": "healthy"}