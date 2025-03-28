import os
from dotenv import load_dotenv


# .env 파일 로드
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    CHUNK_SIZE = os.getenv("CHUNK_SIZE", 500)
    CHUNK_OVERLAP = os.getenv("CHUNK_OVERLAP", 100)

    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "TEST")
    
    CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", None)

    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
    LLM_SYSTEM_ROLE = os.getenv("LLM_SYSTEM_ROLE", "You are a helpful, knowledgeable, and concise assistant. Provide clear and accurate answers to the user's questions")
    
main_config = Config()