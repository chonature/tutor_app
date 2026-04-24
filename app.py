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

# 2. 모델 설정 (시스템 프롬프트를 모델 초기화 시에 주입합니다)
system_prompt = "너는 초등학교 데이터 분석 튜터야. 정답을 바로 주지 말고 CoT(생각의 사슬) 방식으로 질문하며 유도해."
model = genai.GenerativeModel(
    model_name='gemini-3.1-pro-preview',
    system_instruction=system_prompt # 여기에 시스템 프롬프트를 넣습니다.
) 

# 3. 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. 기존 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 처리 및 AI 응답
if prompt := st.chat_input("무엇을 도와줄까?"):
    # 사용자 메시지 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성 (예외 처리 포함)
    with st.chat_message("assistant"):
        try:
            # ⭐ 핵심 변경 사항: Streamlit의 대화 기록을 Gemini API 형식에 맞게 변환
            # Streamlit은 'assistant'를 쓰지만, Gemini는 'model'을 씁니다.
            gemini_history = []
            
            # 방금 st.session_state에 추가한 '현재 질문'은 제외하고 이전 기록만 불러옵니다.
            for msg in st.session_state.messages[:-1]:
                role = "model" if msg["role"] == "assistant" else "user"
                gemini_history.append({"role": role, "parts": [msg["content"]]})

            # 이전 대화 기록을 담아 Gemini 채팅 세션을 시작합니다.
            chat = model.start_chat(history=gemini_history)
            
            # 현재 질문을 전송하여 답변을 받습니다.
            response = chat.send_message(prompt)
            
            # 화면에 출력 및 세션에 저장
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except exceptions.ResourceExhausted:
            st.error("앗! 지금 질문이 너무 많아 서버가 바빠요. 잠시만 기다렸다가 다시 시도해 주세요!")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
