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
        height: 35px;
        width: 35px;
        font-size: 0px;
        font-weight: bold;
        margin: 1px;
        padding: 0;
        min-width: 35px;
    }
    div[data-testid="column"] {
        padding: 1px;
    }
    .block-container {
        padding: 1rem;
        max-width: 100%;
    }
    h1 {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    h2 {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        margin-bottom: 0.3rem;
    }
    h3 {
        font-size: 1rem;
        margin: 0.3rem 0;
    }
    /* 파티원 그룹 간격 */
    div[data-testid="column"]:nth-child(2),
    div[data-testid="column"]:nth-child(3),
    div[data-testid="column"]:nth-child(4),
    div[data-testid="column"]:nth-child(5) {
        margin-left: 15px;
    }
</style>
""", unsafe_allow_html=True)

# 제목
st.title("🎭 로미오와 줄리엣 PQ 6단계")

# 초기화 버튼
if st.button("🔄 초기화", use_container_width=False):
    st.session_state.answers = [[0 for _ in range(4)] for _ in range(10)]
    st.rerun()

st.markdown("---")

# 헤더: 층 + 파티원 1~4
header_cols = st.columns([0.5, 1, 1, 1, 1])
with header_cols[0]:
    st.markdown("**층**")
for i in range(4):
    with header_cols[i + 1]:
        st.markdown(f"**P{i + 1}**")

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
    row_cols = st.columns([0.5, 1, 1, 1, 1])
    
    # 층 번호
    with row_cols[0]:
        st.markdown(f"<div style='text-align: center; padding-top: 8px; font-weight: bold;'>{floor + 1}</div>", unsafe_allow_html=True)
    
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
                        button_label = ""
                        button_type = "primary"
                        disabled = False
                    elif is_locked:
                        button_label = ""
                        button_type = "secondary"
                        disabled = True
                    else:
                        button_label = ""
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
    
    st.markdown("")  # 층 사이 간격

# 하단 요약 (간단하게)
st.markdown("---")
st.markdown("**📊 진행 상황**")

for floor in range(10):
    answers_text = []
    for party_idx in range(4):
        answer = st.session_state.answers[floor][party_idx]
        if answer == 0:
            answers_text.append("-")
        else:
            answers_text.append(str(answer))
    st.text(f"{floor + 1}층: {' | '.join(answers_text)}")

# 사용 방법
with st.expander("ℹ️ 사용법"):
    st.markdown("""
    **클릭하여 발판 선택**
    - 파란색: 선택한 정답
    - 회색: 사용 불가 (다른 파티원이 선택)
    - 흰색: 선택 가능
    
    **규칙**: 각 층마다 4명이 서로 다른 발판 사용
    """)