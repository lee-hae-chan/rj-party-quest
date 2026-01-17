import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="로미오와 줄리엣 파티퀘스트 6단계", layout="wide")

# 세션 상태 초기화
if 'answers' not in st.session_state:
    # answers[층][파티원] = 정답 발판 번호 (0은 미선택)
    st.session_state.answers = [[0 for _ in range(4)] for _ in range(10)]

if 'current_floor' not in st.session_state:
    st.session_state.current_floor = 1

# 제목
st.title("로미오와 줄리엣 파티퀘스트 6단계 도우미")
st.markdown("---")

# 사이드바 - 층 선택
st.sidebar.header(" 설정")
current_floor = st.sidebar.selectbox(
    "현재 층",
    range(1, 11),
    index=st.session_state.current_floor - 1
)
st.session_state.current_floor = current_floor

if st.sidebar.button("전체 초기화"):
    st.session_state.answers = [[0 for _ in range(4)] for _ in range(10)]
    st.rerun()

if st.sidebar.button("현재 층 초기화"):
    floor_idx = current_floor - 1
    st.session_state.answers[floor_idx] = [0, 0, 0, 0]
    st.rerun()

# 메인 화면
st.header(f"📍 {current_floor}층")
st.markdown("**파티원의 발판을 클릭하면 다른 파티원들의 해당 발판이 자동으로 잠깁니다.**")
st.markdown("---")

floor_idx = current_floor - 1

# 현재 층의 정답들 수집
used_platforms = {}  # {발판번호: 파티원번호}
for party_member in range(4):
    answer = st.session_state.answers[floor_idx][party_member]
    if answer != 0:
        used_platforms[answer] = party_member

# 4명의 파티원을 가로로 배치
cols = st.columns(4)

for party_idx in range(4):
    with cols[party_idx]:
        st.markdown(f"### 파티원 {party_idx + 1}")
        
        my_answer = st.session_state.answers[floor_idx][party_idx]
        
        # 4개의 발판 버튼
        for platform in range(1, 5):
            # 버튼 상태 결정
            is_my_answer = (my_answer == platform)
            is_locked = (platform in used_platforms and used_platforms[platform] != party_idx)
            
            # 버튼 스타일 및 텍스트
            if is_my_answer:
                button_label = f"{platform}번 발판 (정답)"
                button_type = "primary"
            elif is_locked:
                button_label = f"{platform}번 발판 (사용됨)"
                button_type = "secondary"
            else:
                button_label = f"{platform}번 발판"
                button_type = "secondary"
            
            # 버튼 클릭 처리
            if st.button(
                button_label,
                key=f"floor_{current_floor}_party_{party_idx}_platform_{platform}",
                disabled=is_locked,
                type=button_type,
                use_container_width=True
            ):
                if is_my_answer:
                    # 이미 선택된 발판을 다시 클릭하면 선택 해제
                    st.session_state.answers[floor_idx][party_idx] = 0
                else:
                    # 새로운 발판 선택
                    st.session_state.answers[floor_idx][party_idx] = platform
                st.rerun()
        
        st.markdown("---")

st.markdown("---")

# 전체 진행 상황
st.header("📋 전체 진행 상황")

# 데이터프레임 생성
progress_data = []
for floor in range(10):
    row = [f"{floor+1}층"]
    for party in range(4):
        answer = st.session_state.answers[floor][party]
        if answer == 0:
            row.append("-")
        else:
            row.append(f"{answer}번")
    progress_data.append(row)

df = pd.DataFrame(
    progress_data,
    columns=["층", "1번", "2번", "3번", "4번"]
)

st.dataframe(df, use_container_width=True, height=400)

# 사용 방법 안내
with st.expander("사용 방법"):
    st.markdown("""
    ### 사용 방법
    
    1. **현재 층 선택**: 왼쪽 사이드바에서 진행 중인 층을 선택하세요.
    
    2. **발판 클릭**: 
       - 각 파티원이 통과한 발판 번호를 **클릭**하세요.
       - 예: 파티원 1이 3번 발판으로 통과했다면 → 파티원 1 아래의 "3번 발판" 클릭
    
    3. **자동 잠금**: 
       - 한 파티원이 발판을 선택하면 다른 파티원들의 같은 번호 발판이 자동으로 잠깁니다.
       -  녹색: 선택한 정답 발판
       -  회색: 다른 파티원이 사용 중 (선택 불가)
       -  흰색: 선택 가능한 발판
    
    4. **선택 해제**: 정답 발판을 다시 클릭하면 선택이 해제됩니다.
    
    5. **초기화**: 
       - 현재 층만 초기화: "현재 층 초기화" 버튼
       - 전체 초기화: "전체 초기화" 버튼
    
    ### 핵심 규칙
    - 각 층마다 4개의 발판이 있습니다.
    - 한 파티원이 특정 발판으로 통과하면, 다른 파티원들은 그 발판을 사용할 수 없습니다.
    - 모든 파티원이 서로 다른 발판으로 통과해야 합니다.
    """)