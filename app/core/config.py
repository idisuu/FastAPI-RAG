import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

config = Config()