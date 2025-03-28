from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser

from app.core.configs.config import main_config

class GenerateService:
    def __init__(self):
        self.chat_prompt = ChatPromptTemplate.from_messages([
            ("system", main_config.LLM_SYSTEM_ROLE),
            ("user", "{query}"),
        ])
        self.llm = ChatOpenAI(model=main_config.LLM_MODEL, api_key=main_config.OPENAI_API_KEY)
        self.parser = StrOutputParser()
        self.chain = self.chat_prompt | self.llm | self.parser

    def generate(self, query):
        # ChatOpenAI는 메시지 리스트를 입력으로 받습니다.
        messages = {"query": query}
        result = self.chain.invoke(messages)
        return result

def get_generate_service():
    # 전역 객체를 반환하여 DI(의존성 주입)용으로 사용합니다.
    return generate_service

generate_service = GenerateService()