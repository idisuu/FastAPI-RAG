from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser

from app.core.configs.config import main_config
from app.core.utils.logger import logger

class GenerateService:
    def __init__(self):
        self.chat_prompt = ChatPromptTemplate.from_messages([
            ("system", main_config.LLM_SYSTEM_ROLE),
            ("user", "다음 문서들을 참고하세요:\n{docs}\n\n질문: {query}"),
        ])
        self.llm = ChatOpenAI(model=main_config.LLM_MODEL, api_key=main_config.OPENAI_API_KEY)
        self.parser = StrOutputParser()
        self.chain = self.chat_prompt | self.llm | self.parser

    def generate(self, query, vectordb, use_rag):
        # ChatOpenAI는 메시지 리스트를 입력으로 받습니다.
        if use_rag:
            docs = vectordb.similarity_search_with_score(query, k=main_config.NUM_RAG_REFERENCE)
            docs_content = "\n\n".join(
                [f"==== 문서 {i+1} ====\n{doc[0].page_content}" for i, doc in enumerate(docs)]
            )
        else:
            docs_content = ""
            
         # 프롬프트 템플릿의 변수에 맞춰 메시지를 구성합니다.
        messages = {"docs": docs_content, "query": query}        
        logger.debug(messages)
        result = self.chain.invoke(messages)
        return result

def get_generate_service():
    # 전역 객체를 반환하여 DI(의존성 주입)용으로 사용합니다.
    return generate_service

generate_service = GenerateService()