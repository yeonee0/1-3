import streamlit as st
import json
import os
from datetime import datetime, date

DATA_FILE = "data.json"

# 데이터 불러오기
def load_tasks():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

st.set_page_config(
    page_title="수행평가 정리",
    page_icon="📚"
)

st.title("📚 수행평가 정리")

tasks = load_tasks()

today = date.today()

if not tasks:
    st.info("등록된 수행평가가 없습니다.")
else:
    for task in tasks:
        try:
            target_date = datetime.strptime(
                task["date"],
                "%Y-%m-%d"
            ).date()

            dday = (target_date - today).days

            if dday > 0:
                dday_text = f"D-{dday}"
            elif dday == 0:
                dday_text = "D-DAY"
            else:
                dday_text = f"D+{abs(dday)}"

            st.write(
                f"📖 {task['subject']} | 📅 {task['date']} | 🔥 {dday_text}"
            )

        except Exception as e:
            st.error(f"데이터 오류: {e}")
