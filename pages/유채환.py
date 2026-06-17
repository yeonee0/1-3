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
def calculate_priority(task_duedate, task_difficulty):
    today = date.today()
    remaining_days = (task_duedate - today).days
    if remaining_days < 0:
        return -1.0
    # 공식: (난이도 * 10) / (남은 일수 + 1)
    score = (task_difficulty * 10) / (remaining_days + 1)
    return round(score, 1)

# --- 메인 화면 레이아웃 ---
st.title("📝 고등학교 수행평가 우선순위 플래너")
st.caption("마감일과 난이도를 분석하여 지금 가장 먼저 해야 할 수행평가를 알려줍니다!")
st.markdown("---")

# 왼쪽 사이드바: 신규 수행평가 등록
with st.sidebar:
    st.header("➕ 수행평가 추가하기")
    
    with st.form(key="task_form", clear_on_submit=True):
        input_subject = st.text_input("과목명", placeholder="예: 국어, 화학 I")
        input_title = st.text_input("수행평가 제목", placeholder="예: 보고서 제출, 발표 준비")
        input_duedate = st.date_input("마감일 선택", min_value=date.today())
        input_difficulty = st.slider("내가 느끼는 난이도", min_value=1, max_value=5, value=3)
        input_memo = st.text_area("메모/주의사항", placeholder="팀원 정보, 준비물 등")
        
        submit_button = st.form_submit_button(label="플래너에 추가")
        
        if submit_button:
            if not input_subject.strip() or not input_title.strip():
                st.error("과목명과 수행평가 제목을 입력해주세요!")
            else:
                if len(st.session_state.tasks) > 0:
                    new_id = max([t["id"] for t in st.session_state.tasks]) + 1
                else:
                    new_id = 1
                    
                new_task = {
                    "id": new_id,
                    "subject": input_subject.strip(),
                    "title": input_title.strip(),
                    "duedate": input_duedate,
                    "difficulty": input_difficulty,
                    "status": "대기 중",
                    "memo": input_memo.strip()
                }
                st.session_state.tasks.append(new_task)
                st.success("새로운 수행평가가 등록되었습니다!")
                st.rerun()

# 우측 메인 영역: 상태 대시보드 및 리스트
if not st.session_state.tasks:
    st.info("현재 등록된 수행평가가 없습니다. 왼쪽 사이드바에서 첫 수행평가를 등록해보세요! 🎉")
else:
    # 데이터 가공 및 우선순위 계산
    processed_list = []
    for t in st.session_state.tasks:
        t_copy = dict(t)
        today_val = date.today()
        rem = (t_copy["duedate"] - today_val).days
        t_copy["remaining"] = rem
        t_copy["priority_score"] = calculate_priority(t_copy["duedate"], t_copy["difficulty"])
        processed_list.append(t_copy)
    
    df = pd.DataFrame(processed_list)
    
    # 상단 대시보드 메트릭 표시
    c_waiting = len(df[df["status"] == "대기 중"])
    c_ongoing = len(df[df["status"] == "진행 중"])
    c_done = len(df[df["status"] == "완료"])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("⏳ 대기 중", c_waiting)
    col2.metric("🏃 진행 중", c_ongoing)
    col3.metric("✅ 완료됨", c_done)
    
    st.markdown("### 🔥 지금 당장 시작해야 할 수행평가 (우선순위 순)")
    
    # 진행 중/대기 중인 스케줄만 필터링 후 정렬
    df_active = df[df["status"] != "완료"]
    if len(df_active) > 0:
        df_active = df_active.sort_values(by=["priority_score", "remaining"], ascending=[False, True])
        
        for idx, row in df_active.iterrows():
            r_id = row["id"]
            r_subject = row["subject"]
            r_title = row["title"]
            r_rem = row["remaining"]
            r_score = row["priority_score"]
            r_diff = row["difficulty"]
            r_memo = row["memo"]
            r_status = row["status"]
            
            # 안내 문구 설정
            if r_rem <= 2:
                st.error(f"🔴 마감 임박!! [{r_subject}] {r_title} (D-{r_rem})")
            elif r_rem <= 5:
                st.warning(f"🟡 주의 [{r_subject}] {r_title} (D-{r_rem})")
            else:
                st.info(f"🟢 안정 [{r_subject}] {r_title} (D-{r_rem})")
            
            # 상세 수치 출력
            d_col1, d_col2, d_col3, d_col4 = st.columns([2, 2, 2, 2])
            d_col1.write(f"📅 **마감일**: {row['duedate']}")
            d_col2.write(f"💪 **난이도**: {'★' * r_diff}")
            d_col3.write(f"⚡ **우선순위 점수**: {r_score}점")
            
            with d_col4:
                opts = ["대기 중", "진행 중", "완료"]
                try:
                    init_idx = opts.index(r_status)
                except ValueError:
                    init_idx = 0
                
                selected_status = st.selectbox(
                    "상태 변경",
                    opts,
                    index=init_idx,
                    key=f"sel_{r_id}"
                )
                
                # 상태 변경 시 즉시 반영
                if selected_status != r_status:
                    for original_task in st.session_state.tasks:
                        if original_task["id"] == r_id:
                            original_task["status"] = selected_status
                            st.rerun()
            
            if r_memo:
                st.caption(f"📝 메모: {r_memo}")
            st.markdown("---")
    else:
        st.success("할 일을 모두 끝냈습니다! 멋져요! 😎")
        
    # 완료된 항목 관리 단락 (가장 안전한 문자열 결합 구조로 변경)
    df_completed = df[df["status"] == "완료"]
    if len(df_completed) > 0:
        with st.expander("✅ 완료된 수행평가 목록 확인 및 삭제"):
            for idx, row in df_completed.iterrows():
                comp_id = row["id"]
                comp_subject = row["subject"]
                comp_title = row["title"]
                
                cc1, cc2 = st.columns([8, 2])
                cc1.write(f"✓ [{comp_subject}] {comp_title}")
                
                if cc2.button("🗑️ 영구 삭제", key=f"del_{comp_id}"):
                    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != comp_id]
                    st.rerun()
