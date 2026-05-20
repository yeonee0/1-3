# schedule_app.py
import streamlit as st
from datetime import date

st.title("간단 스케줄 관리 앱")

# 날짜 선택
selected_date = st.date_input("날짜 선택", date.today())

# 할 일 입력
task = st.text_input("오늘 할 일 입력")

# 입력 버튼
if st.button("추가"):
    if "tasks" not in st.session_state:
        st.session_state.tasks = {}  # 날짜별 할 일 저장
    if selected_date not in st.session_state.tasks:
        st.session_state.tasks[selected_date] = []
    if task:
        st.session_state.tasks[selected_date].append(task)
        st.success(f"{task} 추가 완료!")

# 선택한 날짜의 할 일 표시
st.subheader(f"{selected_date}의 할 일")
if "tasks" in st.session_state and selected_date in st.session_state.tasks:
    for i, t in enumerate(st.session_state.tasks[selected_date], start=1):
        st.write(f"{i}. {t}")
else:
    st.write("할 일이 없습니다.")
