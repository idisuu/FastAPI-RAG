import streamlit as st
import requests

import os

# FastAPI 서버 주소 (예: 로컬에서 실행 중인 경우)
BASE_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

st.title("FastAPI와 Streamlit 연동")

# 파일 등록(Enroll) 섹션
st.header("파일 등록")
uploaded_file = st.file_uploader("파일을 업로드하세요", type=["txt", "pdf", "docx", "png", "jpg"])
if uploaded_file is not None:
    if st.button("파일 등록"):
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
        }
        try:
            with st.spinner("파일 등록 중..."):
                response = requests.post(f"{BASE_URL}/enroll/file", files=files)
            if response.ok:
                st.success("파일 등록 성공!")
            else:
                st.error(f"등록 실패: {response.text}")
        except Exception as e:
            st.error(f"요청 중 오류 발생: {e}")

# 문서 조회(Registered Files) 섹션
st.header("등록된 파일 목록 조회")
if st.button("문서 조회"):
    try:
        with st.spinner("문서 목록 조회 중..."):
            response = requests.get(f"{BASE_URL}/enroll/registered-files")
        if response.ok:
            # 다운로드 링크와 함께 등록된 파일 이름 목록을 출력합니다.
            st.subheader("등록된 파일 목록")
            # Textarea 위젯을 사용해 내용을 보여주면 스크롤도 지원됩니다.
            st.text_area("파일 목록", response.text, height=300)
            # st.download_button을 사용해 다운로드 기능을 추가할 수도 있습니다.
            st.download_button(
                label="파일 목록 다운로드",
                data=response.text,
                file_name="registered_files.txt",
                mime="text/plain"
            )
        else:
            st.error(f"문서 조회 실패: {response.text}")
    except Exception as e:
        st.error(f"요청 중 오류 발생: {e}")

# 텍스트 생성(Generate) 섹션
st.header("텍스트 생성")
query = st.text_input("생성할 텍스트에 대한 쿼리를 입력하세요")
use_rag = st.checkbox("RAG 사용 여부", value=True)
if st.button("생성"):
    if not query:
        st.error("쿼리를 입력해주세요")
    else:
        try:
            params = {
                "query": query,
                "use_rag": use_rag
            }
            with st.spinner("텍스트 생성 중..."):
                response = requests.post(f"{BASE_URL}/generate", params=params)
            if response.ok:
                result_data = response.json()                
                st.subheader("생성 결과")
                st.write(result_data["result"])
                if use_rag and "related_files" in result_data:
                    st.subheader("관련 문서 다운로드")
                    for fname in result_data["related_files"]:                        
                        pdf_url = f"{BASE_URL}/{fname}"
                        st.markdown(f"[📄 {fname} 다운로드]({pdf_url})", unsafe_allow_html=True)
            else:
                st.error(f"생성 실패: {response.text}")
        except Exception as e:
            st.error(f"요청 중 오류 발생: {e}")
