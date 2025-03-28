import io
import re
from typing import BinaryIO, List

from fastapi import HTTPException

import fitz  # PyMuPDF

from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.core.configs.config import main_config
from app.core.utils.logger import logger

CONTROL_CHARS = [
    '\u202a', '\u202b', '\u202c', '\u202d', '\u202e',  # 방향 제어 문자들
    '\u200e', '\u200f'  # LRM, RLM
]
CONTROL_CHAR_PATTERN = re.compile('|'.join(map(re.escape, CONTROL_CHARS)))

ALLOWED_EXTENSIONS = {"pdf"}

class EnrollService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = main_config.CHUNK_SIZE,
            chunk_overlap = main_config.CHUNK_OVERLAP,
            length_function = len,
        )

    def load_pdf_from_bytes(self, content: bytes):
        # 파일 내용을 읽고 메모리 스트림으로 감쌈
        pdf_stream = io.BytesIO(content)

        # PyMuPDF로 PDF 열기
        doc = fitz.open("pdf", pdf_stream)

        # langchain 형식으로 페이지마다 Document 생성
        documents = []
        for i, page in enumerate(doc):
            text = page.get_text()
            clean_text = CONTROL_CHAR_PATTERN.sub('', text)
            metadata = {"page": i + 1}
            documents.append(Document(page_content=clean_text, metadata=metadata))
            
        return documents

    def split_text(self, text: str):
        return self.text_splitter.split_text(text)

    def register(self, vectordb, docs: List[Document]):
        """
        각 텍스트 청크에 대해 Document 객체를 받아,
        OpenAIEmbeddings를 사용하여 임베딩을 생성하고
        Chroma 벡터 스토어에 등록합니다.
        """
        # 문서 리스트가 비어 있지 않은지 확인 후 등록
        if docs:
            vectordb.add_documents(docs)
        else:
            logger.warning("등록할 문서가 없습니다.")
        return {"status": "success"}

    def enroll(self, content: bytes, vectordb, file_name, extension):
        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"{extension} 확장자는 등록할 수 없습니다. 가능한 확장자 : [{', '.join(ALLOWED_EXTENSIONS)}]")

        if extension == "pdf":
            documents = self.load_pdf_from_bytes(content)            
            
        all_chunks = []
        for doc in documents:                
            chunks = self.split_text(doc.page_content)
            for chunk in chunks:
                all_chunks.append(Document(page_content=chunk, metadata=doc.metadata))

        # split된 텍스트들을 Chroma를 사용해 등록
        status = self.register(vectordb, all_chunks)            
        
        logger.info(f"CHROMA의 {main_config.COLLECTION_NAME} collection에 [{file_name}]문서의 {len(all_chunks)}개 chunk가 등록되었습니다.")
        count_info = vectordb._collection.count()
        logger.info(f"전체 저장된 문서 수: {count_info}")

        return {"status": "success"}
            
# 전역 인스턴스 대신, DI를 위한 함수 정의
def get_enroll_service():
    return enroll_service  # 이미 생성된 전역 인스턴스 사용 가능

enroll_service = EnrollService()