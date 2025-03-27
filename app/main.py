from fastapi import FastAPI

from app.routers.common import common_router
from app.core.utils.logger import logger

app = FastAPI()

logger.info("="*100)
logger.info("App Started")
logger.info("="*100)

app.include_router(common_router)