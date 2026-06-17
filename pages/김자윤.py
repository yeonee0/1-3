import streamlit as st
import pandas as pd
from datetime import datetime

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="수행평가 관리 도우미",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# -----------------------------
# 함수
# -----------------------------
def add_task(subject, task_name, due_date, total_score, current_score, importance):
    st.session_state.tasks.append({
        "과목명": subject,
        "수행평가명": task_name,
        "마감일": due_date,
        "배점": total_score,
        "현재점수": current_score,
        "중요도": importance
    })

def get_dataframe():
    if not st.session_state.tasks:
        return pd.DataFrame()

    df = pd.DataFrame(st.session_state.tasks)

    df["진행률(%)"] = df.apply(
        lambda row: round(
            (row["현재점수"] / row["배점"]) * 100, 1
        ) if row["배점"] > 0 else 0,
        axis=1
    )

    return df

# -----------------------------
# 제목
# -----------------------------
st.title("📚 수행평가 관리 도우미")
st.markdown("### 수행평가 일정과 점수를 한눈에 관리하세요.")

# -----------------------------
# 사이드바 메뉴
# -----------------------------
menu = st.sidebar.radio(
    "메뉴 선택",
    ["대시보드", "수행평가 추가", "수행평가 목록"]
)

# -----------------------------
# 수행평가 추가
# -----------------------------
if menu == "수행평가 추가":

    st.header("➕ 수행평가 추가")

    with st.form("add_form"):

        subject = st.text_input("과목명")
        task_name = st.text_input("수행평가명")
        due_date = st.date_input("마감일")

        col1, col2 = st.columns(2)

        with col1:
            total_score = st.number_input(
                "배점",
                min_value=0,
                value=100
            )

        with col2:
            current_score = st.number_input(
                "현재 점수",
                min_value=0,
                value=0
            )

        importance = st.selectbox(
            "중요도",
            ["상", "중", "하"]
        )

        submitted = st.form_submit_button("저장")

        if submitted:

            if not subject.strip():
                st.error("과목명을 입력하세요.")
            elif not task_name.strip():
                st.error("수행평가명을 입력하세요.")
            else:
                add_task(
                    subject,
                    task_name,
                    due_date,
                    total_score,
                    current_score,
                    importance
                )

                st.success("수행평가가 추가되었습니다.")

# -----------------------------
# 수행평가 목록
# -----------------------------
elif menu == "수행평가 목록":

    st.header("📋 수행평가 목록")

    df = get_dataframe()

    if df.empty:
        st.info("등록된 수행평가가 없습니다.")
    else:

        st.dataframe(
            df,
            use_container_width=True
        )

        st.subheader("🗑️ 수행평가 삭제")

        options = [
            f"{row['과목명']} - {row['수행평가명']}"
            for _, row in df.iterrows()
        ]

        selected = st.selectbox(
            "삭제할 수행평가 선택",
            options
        )

        if st.button("삭제"):

            index = options.index(selected)
            del st.session_state.tasks[index]

            st.success("삭제되었습니다.")
            st.rerun()

# -----------------------------
# 대시보드
# -----------------------------
elif menu == "대시보드":

    st.header("📊 대시보드")

    df = get_dataframe()

    if df.empty:
        st.info("등록된 수행평가가 없습니다.")
    else:

        # 평균 점수
        avg_score = round(df["현재점수"].mean(), 1)

        best_subject = (
            df.groupby("과목명")["현재점수"]
            .mean()
            .idxmax()
        )

        worst_subject = (
            df.groupby("과목명")["현재점수"]
            .mean()
            .idxmin()
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "전체 평균 점수",
            avg_score
        )

        col2.metric(
            "최고 점수 과목",
            best_subject
        )

        col3.metric(
            "최저 점수 과목",
            worst_subject
        )

        st.divider()

        # 마감 임박 알림
        st.subheader("⏰ 마감 임박 알림")

        today = datetime.today().date()

        for _, row in df.iterrows():

            due = row["마감일"]

            if hasattr(due, "to_pydatetime"):
                due = due.to_pydatetime().date()

            days_left = (due - today).days

            if days_left <= 3:
                st.error(
                    f"{row['과목명']} - {row['수행평가명']} "
                    f"({days_left}일 남음)"
                )

            elif days_left <= 7:
                st.warning(
                    f"{row['과목명']} - {row['수행평가명']} "
                    f"({days_left}일 남음)"
                )

        st.divider()

        # 과목별 평균 점수
        st.subheader("📈 과목별 평균 점수")

        subject_avg = (
            df.groupby("과목명")["현재점수"]
            .mean()
        )

        st.bar_chart(subject_avg)

        # 중요도별 개수
        st.subheader("⭐ 중요도별 개수")

        importance_count = (
            df["중요도"]
            .value_counts()
        )

        st.bar_chart(importance_count)
