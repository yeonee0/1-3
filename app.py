import streamlit as st
import json
import os
from datetime import date

# 페이지 설정
st.set_page_config(
    page_title="수행평가 정리",
    page_icon="📚",
    layout="wide"
)

DATA_FILE = "data.json"


# 데이터 불러오기
def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except:
        return []


# 데이터 저장
def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        st.error("데이터 저장 중 오류가 발생했습니다.")


tasks = load_data()

# 사이드바 메뉴
menu = st.sidebar.radio(
    "메뉴 선택",
    ["🏠 메인", "➕ 수행평가 추가"]
)

# -------------------
# 메인 페이지
# -------------------
if menu == "🏠 메인":

    st.title("📚 수행평가 정리")

    if not tasks:
        st.info("등록된 수행평가가 없습니다.")
    else:

        today = date.today()

        sorted_tasks = sorted(
            tasks,
            key=lambda x: (
                date.fromisoformat(x["deadline"]) - today
            ).days
        )

        st.subheader("다가오는 수행평가")

        for idx, task in enumerate(sorted_tasks):

            deadline = date.fromisoformat(task["deadline"])
            d_day = (deadline - today).days

            if d_day > 0:
                dday_text = f"D-{d_day}"
                color = "#e8f5e9"
            elif d_day == 0:
                dday_text = "🔥 오늘 마감"
                color = "#fff3cd"
            else:
                dday_text = f"❌ D+{abs(d_day)}"
                color = "#f8d7da"

            st.markdown(
                f"""
                <div style="
                background:{color};
                padding:15px;
                border-radius:10px;
                margin-bottom:10px;">
                    <h4>{task['subject']}</h4>
                    <b>{task['title']}</b><br>
                    마감일: {task['deadline']}<br>
                    <h3>{dday_text}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                f"삭제 - {task['subject']} / {task['title']}",
                key=f"delete_{idx}"
            ):
                tasks.remove(task)
                save_data(tasks)
                st.rerun()

# -------------------
# 추가 페이지
# -------------------
elif menu == "➕ 수행평가 추가":

    st.title("➕ 수행평가 추가")

    with st.form("task_form"):

        subject = st.text_input("과목명")

        title = st.text_input("수행평가명")

        deadline = st.date_input(
            "마감일",
            min_value=date.today()
        )

        submit = st.form_submit_button("저장")

        if submit:

            if not subject.strip():
                st.warning("과목명을 입력하세요.")
            elif not title.strip():
                st.warning("수행평가명을 입력하세요.")
            else:

                tasks.append({
                    "subject": subject.strip(),
                    "title": title.strip(),
                    "deadline": str(deadline)
                })

                save_data(tasks)

                st.success("저장되었습니다!")
