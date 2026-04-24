import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# 1. 기본 설정
st.set_page_config(page_title="😎 보조 탐정 재미니")
st.title("보조 탐정 재미니")
st.write("안녕! 우리 같이 단계적으로 문제를 해결해 나가보자! 나에게 질문해보세요 :)")

# Secrets에서 API 키 호출
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("API Key를 찾을 수 없습니다. Streamlit Cloud의 Secrets 설정을 확인하세요.")
    st.stop()

# 2. 모델 설정 (올바른 모델명 사용 및 시스템 프롬프트 주입)
system_prompt = "너는 초등학교 데이터 분석 튜터야. 정답을 바로 주지 말고 CoT(생각의 사슬) 방식으로 질문하며 유도해."
model = genai.GenerativeModel(
    model_name='gemini-1.5-pro', # 3.1 대신 1.5-pro 또는 1.5-flash 사용
    system_instruction=system_prompt
) 

# 3. 채팅 세션 자체를 초기화하여 저장 (가장 중요한 변경점 ⭐)
if "chat_session" not in st.session_state:
    # 빈 기록으로 채팅 세션을 시작하고, 이 세션 자체를 세션 스테이트에 저장합니다.
    st.session_state.chat_session = model.start_chat(history=[])
    # 화면에 보여주기 위한 메시지 리스트도 별도로 관리합니다.
    st.session_state.messages = []

# 4. 기존 대화 표시 (UI 용도)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 처리 및 AI 응답
if prompt := st.chat_input("무엇을 도와줄까?"):
    
    # UI에 사용자 메시지 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):
        try:
            # 수동으로 history를 만들지 않고, 저장해둔 chat_session 객체를 그대로 사용합니다.
            # send_message를 호출하면 알아서 이전 맥락을 포함하여 답변을 생성하고 기록을 누적합니다.
            response = st.session_
