import streamlit as st
import pandas as pd
from datetime import datetime, date

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="수행평가 ⚡ 우선순위 플래너",
    page_icon="📝",
    layout="wide"
)

# 2. 세션 상태(Session State)를 이용한 데이터 저장소 초기화
if 'tasks' not in st.session_state:
    # 초보자분들이 바로 테스트해볼 수 있도록 샘플 데이터 제공
    st.session_state.tasks = [
        {
            "id": 1,
            "subject": "수학",
            "title": "미적분 탐구 보고서 제출",
            "duedate": date(2026, 6, 25),
            "difficulty": 5,
            "status": "진행 중",
            "memo": "실생활 활용 사례 포함할 것"
        },
        {
            "id": 2,
            "subject": "영어",
            "title": "영미시 암송 및 에세이",
            "duedate": date(2026, 6, 30),
            "difficulty": 3,
            "status": "대기 중",
            "memo": "교과서 12페이지 참고"
        }
    ]

# 3. 우선순위 점수 계산 함수
def calculate_priority(duedate, difficulty):
    today = date.today()
    remaining_days = (duedate - today).days
    if remaining_days < 0:
        return -1  # 이미 마감됨
    # 공식: (난이도 * 10) / (남은 일수 + 1)
    score = (difficulty * 10) / (remaining_days + 1)
    return round(score, 1)

# --- 메인 화면 레이아웃 ---
st.title("📝 고등학교 수행평가 우선순위 플래너")
st.caption("마감일과 난이도를 분석하여 지금 가장 먼저 해야 할 수행평가를 알려줍니다!")
st.markdown("---")

# 왼쪽 사이드바: 신규 수행평가 등록
with st.sidebar:
    st.header("➕ 수행평가 추가하기")
    
    with st.form(key="task_form", clear_on_submit=True):
        subject = st.text_input("과목명", placeholder="예: 국어, 화학 I")
        title = st.text_input("수행평가 제목", placeholder="예: 보고서 제출, 발표 준비")
        duedate = st.date_input("마감일 선택", min_value=date.today())
        difficulty = st.slider("내가 느끼는 난이도", min_value=1, max_value=5, value=3, help="5점에 가까울수록 어렵고 분량이 많음")
        memo = st.text_area("메모/주의사항", placeholder="팀원 정보, 준비물 등")
        
        submit_button = st.form_submit_button(label="플래너에 추가")
        
        if submit_button:
            if not subject.strip() or not title.strip():
                st.error("과목명과 수행평가 제목을 입력해주세요!")
            else:
                new_id = max([t["id"] for t in st.session_state.tasks]) + 1 if st.session_state.tasks else 1
                new_task = {
                    "id": new_id,
                    "subject": subject,
                    "title": title,
                    "duedate": duedate,
                    "difficulty": difficulty,
                    "status": "대기 중",
                    "memo": memo
                }
                st.session_state.tasks.append(new_task)
                st.success(f"'{title}' 수행평가가 등록되었습니다!")
                st.rerun()

# 우측 메인 영역: 상태 대시보드 및 리스트
if not st.session_state.tasks:
    st.info("현재 등록된 수행평가가 없습니다. 왼쪽 사이드바에서 첫 수행평가를 등록해보세요! 🎉")
else:
    # 데이터 가공 및 우선순위 부여
    processed_tasks = []
    for t in st.session_state.tasks:
        task_copy = t.copy()
        today = date.today()
        rem = (task_copy["duedate"] - today).days
        task_copy["remaining"] = rem
        task_copy["priority_score"] = calculate_priority(task_copy["duedate"], task_copy["difficulty"])
        processed_tasks.append(task_copy)
    
    # DataFrame으로 변환 및 정렬 (우선순위 높은 순, 마감일 임박 순)
    df = pd.DataFrame(processed_tasks)
    df_active = df[df["status"] != "완료"].sort_values(by=["priority_score", "remaining"], ascending=[False, True])
    df_completed = df[df["status"] == "완료"]

    # 1. 상단 미니 대시보드
    col1, col2, col3 = st.columns(3)
    col1.metric("⏳ 대기 중", len(df[df["status"] == "대기 중"]))
    col2.metric("🏃 진행 중", len(df[df["status"] == "진행 중"]))
    col3.metric("✅ 완료됨", len(df_completed))
    
    st.markdown("### 🔥 지금 당장 시작해야 할 수행평가 (우선순위 순)")
    
    # 2. 액티브 수행평가 카드 배치
    if len(df_active) == 0:
        st.success("할 일을 모두 끝냈습니다! 멋져요! 😎")
    else:
        for idx, row in df_active.iterrows():
            # D-Day 스타일에 따른 컨테이너 강조
            if row["remaining"] <= 2:
                border_color = "🔴 마감 임박!!"
                st.error(f"**{border_color} [{row['subject']}] {row['title']}** (D-{row['remaining']})")
            elif row["remaining"] <= 5:
                border_color = "🟡 주의"
                st.warning(f"**{border_color} [{row['subject']}] {row['title']}** (D-{row['remaining']})")
            else:
                st.info(f"**🟢 안정 [{row['subject']}] {row['title']}** (D-{row['remaining']})")
            
            # 세부 정보 출력
            c1, c2, c3, c4 = st.columns([2, 2, 2, 2])
            c1.write(f"📅 **마감일**: {row['duedate']}")
            c2.write(f"💪 **난이도**: {'⭐' * row['difficulty']}")
            c3.write(f"⚡ **우선순위 점수**: {row['priority_score']}점")
            
            # 상태 변경 라디오 버튼
            with c4:
                status_options = ["대기 중", "진행 중", "완료"]
                try:
                    current_idx = status_options.index(row["status"])
                except ValueError:
                    current_idx = 0
                    
                new_status = st.selectbox(
                    "상태 변경", 
                    status_options, 
                    index=current_idx, 
                    key=f"status_{row['id']
