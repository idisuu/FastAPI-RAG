# 🔍 FastAPI + Langchain 기반 RAG 프로젝트

이 프로젝트는 **FastAPI**와 **Langchain**을 활용하여 구현된 간단한 **RAG(Retrieval-Augmented Generation)** 서비스입니다.  
사용자의 질의에 대해 관련 문서를 벡터 DB에서 검색한 뒤, OpenAI LLM을 통해 생성된 응답을 제공합니다.

## 🚀 주요 기능
- 사용자 질의 기반 문서 검색 (Vector DB 사용)
- 검색된 문서를 기반으로 LLM 응답 생성
- FastAPI 기반 RESTful API 제공

## 🛠 사용 기술
- Python
- FastAPI
- Langchain
- OpenAI API (ChatGPT)
- 벡터 데이터베이스 (Chroma)

## 🧪 실행 방법

### 🔹 Local 환경에서 실행하기

아래 두 개의 쉘 스크립트를 각각 실행합니다:

```bash
# 백엔드 실행 (FastAPI 서버)
./run_local_backend.sh

# 프론트엔드 실행 (Streamlit 앱)
./run_local_frontend.sh
```

### 🔹 Docker 환경에서 실행하기

Docker Compose를 이용해 전체 서비스를 한 번에 실행할 수 있습니다:

```bash
./run_docker.sh
