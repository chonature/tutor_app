import streamlit as st
import google.generativeai as genai

import streamlit as st
import google.generativeai as genai

# 키가 제대로 들어오는지 확인하는 코드 (안전하게 첫 글자만 확인)
if "API_KEY" in st.secrets:
    st.sidebar.write("API Key가 확인되었습니다.")
else:
    st.sidebar.error("API Key를 찾을 수 없습니다. Secrets 설정을 확인하세요.")
import google.generativeai as genai
from google.api_core import exceptions # 예외 처리를 위해 추가

# ... 기존 코드 ...

try:
    with st.chat_message("assistant"):
        response = genai.generate_content(full_prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

except exceptions.ResourceExhausted:
    st.error("앗! 지금 질문이 너무 많아 서버가 바빠요. 잠시만 기다렸다가 다시 시도해 주세요!")
# 수정 전
# genai.configure(api_key=st.secrets["AIza...길게..."])

# 수정 후
genai.configure(api_key=st.secrets["API_KEY"])
# API 키 설정
# genai.configure(api_key="AIzaSyA1kkmgVagQrHRbO287kAfC0RJjo1yVsxo")

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
if prompt := st.chat_input("무엇을 도와줄까?"):
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
