from fastapi import FastAPI

from app.routers.common import common_router
from app.routers.enroll import enroll_router

from app.core.configs.config import main_config
from app.core.utils.logger import logger
from app.db.chroma_db import init_chroma_db

app = FastAPI()

app.include_router(common_router)
app.include_router(enroll_router)

# startup 이벤트 등록
@app.on_event("startup")
async def startup_event():
    logger.info("="*100)
    logger.info("App Started")
    logger.info("="*100)
    
    for attr in dir(main_config):
        if not attr.startswith("__") and not callable(getattr(main_config, attr)):
            logger.info(f"{attr}: {getattr(main_config, attr)}")
    logger.info("="*100)

    init_chroma_db()

