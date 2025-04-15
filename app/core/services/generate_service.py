import logging
import pprint
from collections import Counter, defaultdict

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
             "참조 표시는 문서의 하단에 한꺼번에 해주세요"
             "사용자는 해당 문서를 직접 다운로드하여 확인할 수 있습니다.\n\n"             
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
            # docs는 (문서, 점수) 튜플의 리스트라고 가정합니다.
            
            # file_name을 키로, (page, page_content)를 값으로 가지는 딕셔너리로 그룹화합니다.
            docs_by_file = defaultdict(list)
            for doc, score in docs:
                file_name = doc.metadata.get('file_name', '문서')
                page = doc.metadata.get('page')
                # 페이지 정보를 int로 변환 (예외 상황에 따라 변환 방식 조정)
                docs_by_file[file_name].append((int(page), doc.page_content))
            
            merged_docs = []
            # 각 file_name별로 정렬 후 연속된 페이지끼리 그룹핑하여 병합합니다.
            for file_name, pages in docs_by_file.items():
                # 페이지 번호 순으로 정렬합니다.
                sorted_pages = sorted(pages, key=lambda x: x[0])
                groups = []
                current_group = []
                current_prev_page = None
    
                for page, content in sorted_pages:
                    if current_prev_page is None:
                        # 첫 번째 페이지인 경우
                        current_group.append((page, content))
                    else:
                        # 현재 페이지가 이전 페이지의 바로 다음이라면 같은 그룹에 추가
                        if page == current_prev_page + 1:
                            current_group.append((page, content))
                        else:
                            groups.append(current_group)
                            current_group = [(page, content)]
                    current_prev_page = page
                if current_group:
                    groups.append(current_group)
    
                # 각 그룹에 대해 페이지 정보(단일 페이지 혹은 범위)를 추가하여 문자열 생성
                for group in groups:
                    pages_in_group = [pg for pg, _ in group]
                    if len(pages_in_group) == 1:
                        page_info = f"페이지: {pages_in_group[0]}"
                    else:
                        page_info = f"페이지: {pages_in_group[0]} ~ {pages_in_group[-1]}"
                    group_content = "\n\n".join(content for _, content in group)
                    merged_docs.append(
                        f"==== 문서 제목: {file_name} ({page_info}) ====\n{group_content}"
                    )
    
            docs_content = "\n\n".join(merged_docs)
            
            file_name_counter = Counter([doc[0].metadata["file_name"] for doc in docs])
            file_names = [file for file, _ in file_name_counter.most_common()]
        else:
            docs_content = ""
            file_names = []
            
         # 프롬프트 템플릿의 변수에 맞춰 메시지를 구성합니다.
        messages = {"docs": docs_content, "query": query}        
        #logger.debug(messages)
        if logger.isEnabledFor(logging.DEBUG):
            print(messages["docs"])
            print("="*100)
            print(messages["query"])
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