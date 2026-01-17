import streamlit as st

# 페이지 설정
st.set_page_config(page_title="로미오와 줄리엣 파티퀘스트 6단계", layout="wide")

# 세션 상태 초기화
if 'answers' not in st.session_state:
    # answers[층][파티원] = 정답 발판 번호 (0은 미선택)
    st.session_state.answers = [[0 for _ in range(4)] for _ in range(10)]

# 제목
st.title("로미오와 줄리엣 파티퀘스트 6단계 도우미")
st.markdown("**파티원의 발판을 클릭하면 같은 층의 다른 파티원들의 해당 발판이 자동으로 잠깁니다.**")

# 초기화 버튼
col1, col2, col3 = st.columns([1, 1, 8])
with col1:
    if st.button("전체 초기화", use_container_width=True):
        st.session_state.answers = [[0 for _ in range(4)] for _ in range(10)]
        st.rerun()

st.markdown("---")

# CSS 스타일
st.markdown("""
<style>
    .stButton button {
        height: 60px;
        font-size: 16px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 10층 모두 표시
for floor in range(10):
    st.subheader(f"{floor + 1}층")
    
    # 현재 층의 사용된 발판 확인
    used_platforms = {}  # {발판번호: 파티원번호}
    for party_idx in range(4):
        answer = st.session_state.answers[floor][party_idx]
        if answer != 0:
            used_platforms[answer] = party_idx
    
    # 파티원 헤더
    header_cols = st.columns(4)
    for i in range(4):
        with header_cols[i]:
            st.markdown(f"**파티원 {i + 1}**")
    
    # 각 발판 행 (1번~4번 발판)
    for platform in range(1, 5):
        platform_cols = st.columns(4)
        
        for party_idx in range(4):
            with platform_cols[party_idx]:
                my_answer = st.session_state.answers[floor][party_idx]
                is_my_answer = (my_answer == platform)
                is_locked = (platform in used_platforms and used_platforms[platform] != party_idx)
                
                # 버튼 텍스트와 타입
                if is_my_answer:
                    button_label = f"{platform}번"
                    button_type = "primary"
                elif is_locked:
                    button_label = f"{platform}번"
                    button_type = "secondary"
                else:
                    button_label = f"{platform}번"
                    button_type = "secondary"
                
                # 버튼 클릭
                if st.button(
                    button_label,
                    key=f"f{floor}_p{party_idx}_pl{platform}",
                    disabled=is_locked,
                    type=button_type,
                    use_container_width=True
                ):
                    if is_my_answer:
                        # 선택 해제
                        st.session_state.answers[floor][party_idx] = 0
                    else:
                        # 선택
                        st.session_state.answers[floor][party_idx] = platform
                    st.rerun()
    
    st.markdown("---")

# 하단 요약
st.header("진행 상황 요약")
summary_text = ""
for floor in range(10):
    floor_summary = f"**{floor + 1}층**: "
    answers_list = []
    for party_idx in range(4):
        answer = st.session_state.answers[floor][party_idx]
        if answer == 0:
            answers_list.append(f"파티원{party_idx + 1}(-)")
        else:
            answers_list.append(f"파티원{party_idx + 1}({answer}번)")
    floor_summary += " | ".join(answers_list)
    st.markdown(floor_summary)

# 사용 방법
with st.expander("사용 방법"):
    st.markdown("""
    ### 사용 방법
    
    1. **발판 클릭하기**:
       - 각 층마다 파티원 1~4의 발판(1번~4번)이 표시됩니다.
       - 파티원이 통과한 발판을 클릭하세요.
       - 예: 1층에서 파티원 1이 3번 발판으로 통과 → "파티원 1" 열의 "3번" 클릭
    
    2. **자동 잠금**:
       - 한 파티원이 발판을 선택하면 **같은 층의** 다른 파티원들은 그 발판을 선택할 수 없습니다.
       - 파란색: 선택한 정답 발판
       - 회색: 다른 파티원이 선택함 (클릭 불가)
       - 흰색: 선택 가능한 발판
    
    3. **선택 해제**:
       - 이미 선택한 발판을 다시 클릭하면 선택이 해제됩니다.
    
    4. **초기화**:
       - 전체 초기화: 상단의 " 전체 초기화" 버튼
    
    ### 핵심 규칙
    - 각 층마다 4개의 발판이 있고, 4명의 파티원이 각각 다른 발판으로 통과해야 합니다.
    - 한 층에서 같은 발판을 2명 이상 사용할 수 없습니다.
    """)