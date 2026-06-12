import streamlit as st
import json
import os
from datetime import datetime, date

DATA_FILE = "data.json"
DONE_FILE = "done.json"

# ---------------- 설정 ----------------
st.set_page_config(page_title="D-Day 수행평가", page_icon="🔥")

# ---------------- 데이터 로드 ----------------
def load_json(file):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

tasks = load_json(DATA_FILE)
done_tasks = load_json(DONE_FILE)

today = date.today()

st.title("📚 수행평가 D-DAY")

# ---------------- 완료 처리 ----------------
def complete_task(task):
    tasks.remove(task)
    done_tasks.append(task)
    save_json(DATA_FILE, tasks)
    save_json(DONE_FILE, done_tasks)
    st.rerun()

# ---------------- 삭제 처리 ----------------
def delete_task(task):
    tasks.remove(task)
    save_json(DATA_FILE, tasks)
    st.rerun()

# ---------------- 메인 D-DAY (핵심) ----------------
if tasks:
    closest_task = min(
        tasks,
        key=lambda x: (datetime.strptime(x["date"], "%Y-%m-%d").date() - today).days
    )

    target_date = datetime.strptime(closest_task["date"], "%Y-%m-%d").date()
    dday = (target_date - today).days

    dday_text = f"D-{dday}" if dday > 0 else ("🔥 D-DAY 🔥" if dday == 0 else f"D+{abs(dday)}")

    # 🔥 당일일 때만 크게 표시
    if dday == 0:
        st.markdown(
            f"""
            <div style="
                text-align:center;
                padding:80px;
                border-radius:30px;
                background:linear-gradient(135deg,#ff0000,#ff7300);
                color:white;
                margin-bottom:30px;
            ">
                <h1 style="font-size:90px;">
                    🔥 {closest_task['subject']} 🔥
                </h1>

                <h1 style="font-size:120px;">
                    {dday_text}
                </h1>

                <p style="font-size:30px;">
                    {closest_task['date']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info(f"다음 수행평가: {closest_task['subject']} ({dday_text})")

# ---------------- 전체 목록 ----------------
st.subheader("📌 전체 수행평가")

if not tasks:
    st.info("남은 수행평가가 없습니다.")
else:
    for task in tasks:
        col1, col2, col3 = st.columns([4, 2, 2])

        with col1:
            st.write(f"📖 {task['subject']} | 📅 {task['date']}")

        with col2:
            if st.button("완료", key=f"done_{task['subject']}_{task['date']}"):
                complete_task(task)

        with col3:
            if st.button("삭제", key=f"del_{task['subject']}_{task['date']}"):
                delete_task(task)

# ---------------- 완료된 목록 ----------------
st.subheader("✅ 완료된 수행평가")

if done_tasks:
    for task in done_tasks:
        st.write(f"✔ {task['subject']} | {task['date']}")
else:
    st.info("완료된 과제가 없습니다.")
