import streamlit as st
import json
import os
from datetime import datetime, date

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

st.title("수행평가 정리")

data = load_data()

if not data:
    st.info("등록된 수행평가가 없습니다.")

else:

    today = date.today()

    for item in data:

        deadline = datetime.strptime(
            item["deadline"],
            "%Y-%m-%d"
        ).date()

        dday = (deadline - today).days

        if dday > 0:
            text = f"D-{dday}"
        elif dday == 0:
            text = "오늘 마감"
        else:
            text = f"D+{abs(dday)}"

        st.markdown(
            f"""
            ### 📚 {item['subject']}
            👤 {item['name']}

            **{text}**
            ---
            """
        )
