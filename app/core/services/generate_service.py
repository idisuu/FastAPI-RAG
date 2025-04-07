from collections import Counter

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser

from app.core.configs.config import main_config
from app.core.utils.logger import logger

class GenerateService:
    def __init__(self):
        self.chat_prompt = ChatPromptTemplate.from_messages([
            ("system", main_config.LLM_SYSTEM_ROLE),
            ("user", 
             "아래 문서들을 참고하여 질문에 답변해 주세요. "
             "답변에 문서 내용을 활용한 경우, 어떤 문서를 참고했는지 명확히 표시해 주세요. "
             "표시는 (문서명 참조) 형식으로 해주세요. 사용자는 해당 문서를 직접 다운로드하여 확인할 수 있습니다.\n\n"             
             "참고 문서:\n{docs}\n\n"
             "질문: {query}")
        ])
        
        self.llm = ChatOpenAI(model=main_config.LLM_MODEL, api_key=main_config.OPENAI_API_KEY)
        self.parser = StrOutputParser()
        self.chain = self.chat_prompt | self.llm | self.parser

    def generate(self, query, vectordb, use_rag):
        # ChatOpenAI는 메시지 리스트를 입력으로 받습니다.
        if use_rag:
            docs = vectordb.similarity_search_with_score(query, k=main_config.NUM_RAG_REFERENCE)
            docs_content = "\n\n".join(
                    [
                        f"==== 문서 제목: {doc[0].metadata.get('file_name', f'문서 {i+1}')} ====\n{doc[0].page_content}"
                        for i, doc in enumerate(docs)
                    ]
            )
            # 관련 file_name 등장 횟수 계산 및 정렬
            file_name_counter = Counter([doc[0].metadata["file_name"] for doc in docs])
            file_names = [file for file, _ in file_name_counter.most_common()]
        else:
            docs_content = ""
            file_names = []
            
         # 프롬프트 템플릿의 변수에 맞춰 메시지를 구성합니다.
        messages = {"docs": docs_content, "query": query}        
        logger.debug(messages)
        result = self.chain.invoke(messages)

        logger.debug(file_names)
        return {
            "result": result,
            "related_files": file_names,
        }

def get_generate_service():
    # 전역 객체를 반환하여 DI(의존성 주입)용으로 사용합니다.
    return generate_service

generate_service = GenerateService()