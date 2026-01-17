import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="로미오와 줄리엣 파티퀘스트 6단계", layout="wide")

# 세션 상태 초기화
if 'answers' not in st.session_state:
    # answers[층][파티원] = 정답 발판 번호 (0은 미입력)
    st.session_state.answers = [[0 for _ in range(4)] for _ in range(10)]

if 'current_floor' not in st.session_state:
    st.session_state.current_floor = 1

# 제목
st.title(" 로미오와 줄리엣 파티퀘스트 6단계 도우미")
st.markdown("---")

# 사이드바 - 층 선택
st.sidebar.header("설정")
current_floor = st.sidebar.selectbox(
    "현재 층",
    range(1, 11),
    index=st.session_state.current_floor - 1
)
st.session_state.current_floor = current_floor

if st.sidebar.button(" 전체 초기화"):
    st.session_state.answers = [[0 for _ in range(4)] for _ in range(10)]
    st.rerun()

# 메인 화면
st.header(f"📍 {current_floor}층")

# 파티원별 입력 섹션
cols = st.columns(4)
floor_idx = current_floor - 1

for i in range(4):
    with cols[i]:
        st.subheader(f"파티원 {i+1}")
        
        # 해당 파티원의 정답 입력
        answer = st.selectbox(
            "정답 발판",
            [0, 1, 2, 3, 4],
            index=st.session_state.answers[floor_idx][i],
            key=f"input_{current_floor}_{i}",
            format_func=lambda x: "선택 안함" if x == 0 else f"{x}번 발판"
        )
        
        if answer != st.session_state.answers[floor_idx][i]:
            st.session_state.answers[floor_idx][i] = answer
            st.rerun()

st.markdown("---")

# 발판 상태 표시
st.header(" 발판 상태")

# 현재 층의 정답들 수집
used_platforms = set()
for party_member in range(4):
    answer = st.session_state.answers[floor_idx][party_member]
    if answer != 0:
        used_platforms.add(answer)

# 각 파티원별로 발판 상태 표시
cols2 = st.columns(4)

for i in range(4):
    with cols2[i]:
        st.markdown(f"**파티원 {i+1}의 가능한 발판**")
        
        # 해당 파티원의 정답
        my_answer = st.session_state.answers[floor_idx][i]
        
        # 발판 1~4 상태 표시
        for platform in range(1, 5):
            if my_answer == platform:
                # 본인의 정답
                st.success(f" {platform}번 발판 (정답)")
            elif platform in used_platforms:
                # 다른 사람이 사용한 발판
                st.error(f" {platform}번 발판")
            else:
                # 아직 사용되지 않은 발판
                st.info(f" {platform}번 발판")

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
    columns=["층", "파티원 1", "파티원 2", "파티원 3", "파티원 4"]
)

st.dataframe(df, use_container_width=True, height=400)

# 사용 방법 안내
with st.expander("ℹ 사용 방법"):
    st.markdown("""
    ### 사용 방법
    
    1. **현재 층 선택**: 왼쪽 사이드바에서 진행 중인 층을 선택하세요.
    
    2. **정답 입력**: 각 파티원이 통과한 발판 번호를 선택하세요.
       - 파티원 1이 1번 발판으로 통과했다면 "파티원 1"에서 "1번 발판" 선택
    
    3. **발판 상태 확인**: 
       -  녹색: 해당 파티원의 정답 발판
       -  빨간색: 다른 파티원이 사용한 발판 (이 파티원은 사용 불가)
       -  파란색: 아직 사용되지 않은 발판 (가능성 있음)
    
    4. **전체 초기화**: 처음부터 다시 시작하려면 사이드바의 "전체 초기화" 버튼을 누르세요.
    
    ### 핵심 규칙
    - 각 층마다 4개의 발판이 있습니다.
    - 한 파티원이 특정 발판으로 통과하면, 다른 파티원들은 그 발판을 사용할 수 없습니다.
    - 모든 파티원이 서로 다른 발판으로 통과해야 합니다.
    """)