import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# 1. 기본 설정 및 API 키 연결
st.set_page_config(page_title="😎 보조 탐정 재미니")
st.title("보조 탐정 재미니")
st.write("안녕! 우리 같이 단계적으로 문제를 해결해 나가보자! 나에게 질문해보세요 :)")

# Secrets에서 API 키 호출 (안전하게)
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("API Key를 찾을 수 없습니다. Streamlit Cloud의 Secrets 설정을 확인하세요.")
    st.stop()

# 모델 설정
model = genai.GenerativeModel('gemini-3.1-pro-preview') 

# 2. 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. 기존 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. 사용자 입력 처리 및 AI 응답
if prompt := st.chat_input("무엇을 도와줄까?"):
    # 사용자 메시지 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 시스템 프롬프트 결합
    system_prompt = "너는 초등학교 데이터 분석 튜터야. 정답을 바로 주지 말고 CoT(생각의 사슬) 방식으로 질문하며 유도해."
    full_prompt = f"{system_prompt}\n\n학생 질문: {prompt}"

    # AI 응답 생성 (예외 처리 포함)
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            # 어시스턴트 메시지 저장
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        
        except exceptions.ResourceExhausted:
            st.error("앗! 지금 질문이 너무 많아 서버가 바빠요. 잠시만 기다렸다가 다시 시도해 주세요!")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
