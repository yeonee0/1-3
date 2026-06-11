import streamlit as st
import json
import os
from datetime import date, datetime

# ---------------------
# 기본 설정
# ---------------------
st.set_page_config(
    page_title="수행평가 정리",
    page_icon="📚",
    layout="wide"
)

DATA_FILE = "data.json"


# ---------------------
# 데이터 불러오기
# ---------------------
def load_tasks():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass

    return []


# ---------------------
# 데이터 저장
# ---------------------
def save_tasks(tasks):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(
                tasks,
                f,
                ensure_ascii=False,
                indent=4
            )
    except Exception as e:
        st.error(f"저장 오류 : {e}")


tasks = load_tasks()

# ---------------------
# 메뉴
# ---------------------
menu = st.sidebar.radio(
    "메뉴",
    [
        "🏠 메인",
        "👤 조윤태 페이지"
    ]
)

# =====================
# 메인 페이지
# =====================
if menu == "🏠 메인":

    st.title("📚 수행평가 정리")

    today = date.today()

    if len(tasks) == 0:
        st.info("등록된 수행평가가 없습니다.")
    else:

        for task in tasks:
            deadline = datetime.strptime(
                task["deadline"],
                "%Y-%m-%d"
            ).date()

            task["dday"] = (deadline - today).days

        tasks.sort(key=lambda x: x["dday"])

        upcoming = [
            t for t in tasks
            if t["dday"] >= 0
        ]

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "남은 수행평가",
                len(upcoming)
            )

        with col2:
            if upcoming:
                st.metric(
                    "가장 가까운 수행평가",
                    upcoming[0]["subject"]
                )

        st.divider()

        for task in tasks:

            dday = task["dday"]

            if dday > 0:
                bg = "#E8F5E9"
                text = f"D-{dday}"

            elif dday == 0:
                bg = "#FFF3CD"
                text = "🔥 오늘 마감"

            else:
                bg = "#F8D7DA"
                text = f"마감 지남 ({abs(dday)}일)"

            st.markdown(
                f"""
                <div style="
                    background:{bg};
                    padding:20px;
                    border-radius:15px;
                    margin-bottom:10px;
                    border:1px solid #ddd;
                ">
                    <h3>{task['subject']}</h3>
                    <p><b>{task['title']}</b></p>
                    <p>📅 {task['deadline']}</p>
                    <h2>{text}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

# =====================
# 조윤태 페이지
# =====================
elif menu == "👤 조윤태.py":

    st.title("👤 조윤태 수행평가 입력")

    with st.form("add_task"):

        subject = st.text_input("과목")

        title = st.text_input("수행평가명")

        deadline = st.date_input(
            "제출일"
        )

        submit = st.form_submit_button(
            "추가하기"
        )

        if submit:

            if not subject.strip():
                st.warning("과목을 입력하세요.")

            elif not title.strip():
                st.warning("수행평가명을 입력하세요.")

            else:

                tasks.append(
                    {
                        "subject": subject.strip(),
                        "title": title.strip(),
                        "deadline": str(deadline)
                    }
                )

                save_tasks(tasks)

                st.success("추가 완료!")

                st.rerun()

    st.divider()

    st.subheader("등록된 수행평가")

    if len(tasks) == 0:
        st.info("등록된 수행평가 없음")

    else:

        for i, task in enumerate(tasks):

            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(
                    f"📚 {task['subject']} | "
                    f"{task['title']} | "
                    f"{task['deadline']}"
                )

            with col2:

                if st.button(
                    "삭제",
                    key=f"delete_{i}"
                ):
                    tasks.pop(i)
                    save_tasks(tasks)
                    st.rerun()
