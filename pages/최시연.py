import streamlit as st
from google import genai
from google.genai import types

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌",
)

st.title("💌 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반 상담 챗봇")

# -----------------------------
# API 키 불러오기
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# -----------------------------
# Gemini 클라이언트 생성
# -----------------------------
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 오류: {e}")
    st.stop()

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요 😊\n"
                "연애 고민이 있다면 편하게 이야기해주세요!"
            ),
        }
    ]

# -----------------------------
# 이전 채팅 표시
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
user_input = st.chat_input("연애 고민을 입력하세요...")

if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            # Gemini용 대화 기록 변환
            history = []

            for msg in st.session_state.messages[:-1]:
                role = "user" if msg["role"] == "user" else "model"

                history.append(
                    types.Content(
                        role=role,
                        parts=[types.Part(text=msg["content"])],
                    )
                )

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=history + [
                    types.Content(
                        role="user",
                        parts=[types.Part(text=user_input)],
                    )
                ],
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    max_output_tokens=500,
                    system_instruction=(
                        "너는 공감 능력이 좋은 연애상담 챗봇이다. "
                        "사용자의 고민을 따뜻하고 현실적으로 상담해줘. "
                        "무조건적인 편들기보다 균형 있게 조언해줘."
                    ),
                ),
            )

            ai_response = response.text

            message_placeholder.markdown(ai_response)

            # 응답 저장
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": ai_response,
                }
            )

        except Exception as e:
            error_message = (
                "⚠️ 오류가 발생했습니다.\n\n"
                f"오류 내용: {str(e)}"
            )

            message_placeholder.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                }
            )

# -----------------------------
# 사이드바 기능
# -----------------------------
with st.sidebar:
    st.header("설정")

    if st.button("대화 초기화"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "안녕하세요 😊 연애 고민을 다시 들려주세요!",
            }
        ]
        st.rerun()

    st.markdown("---")
    st.caption("Model: gemini-2.5-flash-lite")
