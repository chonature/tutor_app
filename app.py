# 5. 사용자 입력 처리 및 AI 응답
if prompt := st.chat_input("무엇을 도와줄까?"):
    
    # UI에 사용자 메시지 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):
        try: # 👈 여기서 try가 시작되었으면
            
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except exceptions.ResourceExhausted: # 👈 같은 들여쓰기 위치에 except가 꼭 있어야 합니다.
            st.error("앗! 지금 질문이 너무 많아 서버가 바빠요. 잠시만 기다렸다가 다시 시도해 주세요!")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
