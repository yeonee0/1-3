import streamlit as st
import json
import os
from datetime import date

DATA_FILE = "data.json"

# 데이터 불러오기
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        tasks = json.load(f)
else:
    tasks = []

st.title("조윤태 수행평가 입력")

subject = st.text_input("과목")
exam_date = st.date_input("수행평가 날짜")

if st.button("저장"):
    tasks.append({
        "subject": subject,
        "date": exam_date.strftime("%Y-%m-%d")
    })

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

    st.success("저장 완료!")
