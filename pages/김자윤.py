import streamlit as st
import json
from datetime import date

st.set_page_config(page_title="수행평가 관리 도우미", layout="wide")

# -----------------------------
# 데이터 초기화
# -----------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# -----------------------------
# 유틸 함수
# -----------------------------
def calculate_progress(tasks):
    if not tasks:
        return 0
    done = sum(1 for t in tasks if t["done"])
    return int((done / len(tasks)) * 100)

def add_task(subject, title, due, weight, memo):
    st.session_state.tasks.append({
        "subject": subject,
        "title": title,
        "due": str(due),
        "weight": weight,
        "memo": memo,
        "done": False,
        "checklist": []
    })

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.title("📌 수행평가 도우미")
menu = st.sidebar.radio("메뉴 선택", ["대시보드", "과제 추가", "데이터 관리"])

# -----------------------------
# 대시보드
# -----------------------------
if menu == "대시보드":
    st.title("📋 수행평가 대시보드")

    progress = calculate_progress(st.session_state.tasks)
    st.progress(progress)
    st.write(f"전체 진행률: **{progress}%**")

    st.divider()

    if not st.session_state.tasks:
        st.info("등록된 수행평가가 없습니다.")
    else:
        for i, task in enumerate(st.session_state.tasks):
            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                st.subheader(task["title"])
                st.write(f"📘 과목: {task['subject']}")
                st.write(f"📅 마감일: {task['due']}")

            with col2:
                st.write(f"📊 비중: {task['weight']}%")
                st.write(f"📝 메모: {task['memo']}")

            with col3:
                done = st.checkbox("완료", value=task["done"], key=f"done_{i}")
                st.session_state.tasks[i]["done"] = done

            # 체크리스트
            with st.expander("체크리스트"):
                new_item = st.text_input("항목 추가", key=f"check_{i}")
                if st.button("추가", key=f"btn_{i}"):
                    if new_item:
                        st.session_state.tasks[i]["checklist"].append(
                            {"text": new_item, "done": False}
                        )
                        st.rerun()

                for j, item in enumerate(task["checklist"]):
                    c1, c2 = st.columns([6, 1])
                    with c1:
                        checked = st.checkbox(
                            item["text"],
                            value=item["done"],
                            key=f"item_{i}_{j}"
                        )
                        st.session_state.tasks[i]["checklist"][j]["done"] = checked

# -----------------------------
# 과제 추가
# -----------------------------
elif menu == "과제 추가":
    st.title("➕ 수행평가 추가")

    with st.form("add_form"):
        subject = st.text_input("과목")
        title = st.text_input("과제 제목")
        due = st.date_input("마감일", value=date.today())
        weight = st.number_input("비중(%)", min_value=0, max_value=100, value=10)
        memo = st.text_area("메모")

        submitted = st.form_submit_button("추가")

        if submitted:
            if subject and title:
                add_task(subject, title, due, weight, memo)
                st.success("과제가 추가되었습니다!")
            else:
                st.error("과목과 제목은 필수입니다.")

# -----------------------------
# 데이터 관리
# -----------------------------
elif menu == "데이터 관리":
    st.title("🧾 데이터 관리")

    st.subheader("⬇️ 데이터 다운로드")

    json_data = json.dumps(st.session_state.tasks, ensure_ascii=False, indent=2)
    st.download_button(
        "JSON 다운로드",
        data=json_data,
        file_name="tasks.json",
        mime="application/json"
    )

    st.subheader("⬆️ 데이터 업로드")

    uploaded = st.file_uploader("JSON 파일 업로드", type=["json"])

    if uploaded:
        try:
            data = json.load(uploaded)
            if isinstance(data, list):
                st.session_state.tasks = data
                st.success("데이터를 불러왔습니다!")
            else:
                st.error("올바른 형식이 아닙니다.")
        except Exception as e:
            st.error(f"오류 발생: {e}")

    st.divider()

    if st.button("⚠️ 전체 데이터 초기화"):
        st.session_state.tasks = []
        st.warning("모든 데이터가 초기화되었습니다.")
