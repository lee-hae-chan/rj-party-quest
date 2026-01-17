import streamlit as st

# 페이지 설정
st.set_page_config(page_title="로미오와 줄리엣 파티퀘스트 6단계", layout="wide")

# 세션 상태 초기화
if 'answers' not in st.session_state:
    # answers[층][파티원] = 정답 발판 번호 (0은 미선택)
    st.session_state.answers = [[0 for _ in range(4)] for _ in range(10)]

# CSS 스타일
st.markdown("""
<style>
    .stButton button {
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        margin: 5px;
    }
    div[data-testid="column"] {
        padding: 10px;
    }
    .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# 제목
st.title("🎭 로미오와 줄리엣 파티퀘스트 6단계 도우미")

# 초기화 버튼
if st.button("🔄 전체 초기화"):
    st.session_state.answers = [[0 for _ in range(4)] for _ in range(10)]
    st.rerun()

st.markdown("---")

# 헤더: 층 + 파티원 1~4
header_cols = st.columns([1, 3, 3, 3, 3])
with header_cols[0]:
    st.markdown("### 층")
for i in range(4):
    with header_cols[i + 1]:
        st.markdown(f"### 👤 파티원 {i + 1}")

st.markdown("---")

# 각 층마다 행 생성
for floor in range(10):
    # 현재 층의 사용된 발판 확인
    used_platforms = {}  # {발판번호: 파티원번호}
    for party_idx in range(4):
        answer = st.session_state.answers[floor][party_idx]
        if answer != 0:
            used_platforms[answer] = party_idx
    
    # 층 번호 + 각 파티원의 4개 발판
    row_cols = st.columns([1, 3, 3, 3, 3])
    
    # 층 번호
    with row_cols[0]:
        st.markdown(f"<h3 style='text-align: center; padding-top: 15px;'>{floor + 1}층</h3>", unsafe_allow_html=True)
    
    # 각 파티원의 발판
    for party_idx in range(4):
        with row_cols[party_idx + 1]:
            my_answer = st.session_state.answers[floor][party_idx]
            
            # 4개 발판을 가로로 배치
            platform_cols = st.columns(4)
            for platform in range(1, 5):
                with platform_cols[platform - 1]:
                    is_my_answer = (my_answer == platform)
                    is_locked = (platform in used_platforms and used_platforms[platform] != party_idx)
                    
                    # 버튼 스타일 결정
                    if is_my_answer:
                        button_label = "✓"
                        button_type = "primary"
                        disabled = False
                    elif is_locked:
                        button_label = "✗"
                        button_type = "secondary"
                        disabled = True
                    else:
                        button_label = str(platform)
                        button_type = "secondary"
                        disabled = False
                    
                    # 버튼 생성
                    if st.button(
                        button_label,
                        key=f"f{floor}_p{party_idx}_pl{platform}",
                        disabled=disabled,
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
    
    st.markdown("<br><br>", unsafe_allow_html=True)  # 층 사이 간격 더 넓게

# 하단 요약
st.markdown("---")
st.header("📊 진행 상황")

summary_cols = st.columns(2)
with summary_cols[0]:
    for floor in range(5):
        answers_text = []
        for party_idx in range(4):
            answer = st.session_state.answers[floor][party_idx]
            if answer == 0:
                answers_text.append("-")
            else:
                answers_text.append(str(answer))
        st.markdown(f"**{floor + 1}층**: " + " | ".join(answers_text))

with summary_cols[1]:
    for floor in range(5, 10):
        answers_text = []
        for party_idx in range(4):
            answer = st.session_state.answers[floor][party_idx]
            if answer == 0:
                answers_text.append("-")
            else:
                answers_text.append(str(answer))
        st.markdown(f"**{floor + 1}층**: " + " | ".join(answers_text))

# 사용 방법
with st.expander("ℹ️ 사용 방법"):
    st.markdown("""
    ### 사용 방법
    
    1. **발판 클릭**:
       - 각 파티원 아래에 1~4번 발판이 있습니다.
       - 통과한 발판 번호를 클릭하세요.
       - 예: 1층에서 파티원 1이 3번 발판으로 통과 → 1층/파티원 1 열의 "3" 클릭
    
    2. **표시 의미**:
       - **숫자 (1~4)**: 선택 가능한 발판
       - **✓ (파란색)**: 내가 선택한 정답 발판
       - **✗ (회색)**: 다른 파티원이 선택함 (클릭 불가)
    
    3. **선택 해제**:
       - ✓ 표시를 다시 클릭하면 선택이 해제됩니다.
    
    4. **자동 잠금**:
       - 한 파티원이 발판을 선택하면 같은 층의 다른 파티원들은 그 발판을 선택할 수 없습니다.
    
    ### 핵심 규칙
    - 각 층마다 4명의 파티원이 각각 다른 발판(1~4번)으로 통과해야 합니다.
    """)