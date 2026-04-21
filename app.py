import streamlit as st
import google.generativeai as genai

# API 키 설정
genai.configure(api_key="AIzaSyA1kkmgVagQrHRbO287kAfC0RJjo1yVsxo")

# 모델 설정
model = genai.GenerativeModel('gemini-3.1-pro-preview')

st.title("보조 탐정 재미니")
st.write("문제를 입력하면 단계별로 생각의 사슬(CoT)을 통해 설명해 드립니다.")

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("문제를 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # CoT를 유도하는 시스템 프롬프트(이전에 작성한 내용)를 결합
    system_prompt = "너는 초등학교 데이터 분석 튜터야. 정답을 바로 주지 말고 CoT 방식으로 질문하며 유도해."
    full_prompt = f"{system_prompt}\n\n학생 질문: {prompt}"

    with st.chat_message("assistant"):
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
    
    st.session_state.messages.append({"role": "assistant", "content": response.text})