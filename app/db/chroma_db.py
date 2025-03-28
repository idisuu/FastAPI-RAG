from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from app.core.configs.config import main_config

# 전역 변수로 사용할 vectordb
vectordb = None

def init_chroma_db():
    global vectordb
    embedding_function = OpenAIEmbeddings()

    documents = []

    # vectordb 인스턴스 생성
    vectordb = Chroma(embedding_function=embedding_function, persist_directory=main_config.CHROMA_PERSIST_DIRECTORY)
    return vectordb

def get_vectordb():
    """의존성 주입을 위해 vectordb 인스턴스를 반환하는 함수"""
    return vectordb