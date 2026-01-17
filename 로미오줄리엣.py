import streamlit as st

# 페이지 설정
st.set_page_config(page_title="로미오와 줄리엣 도우미", layout="wide")

# 세션 상태 초기화
if 'answers' not in st.session_state:
    st.session_state.answers = [[0 for _ in range(4)] for _ in range(10)]

# --- CSS 스타일 (다크 모드 및 버튼 디자인) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    
    /* 버튼 스타일 */
    .stButton button {
        height: 40px;
        width: 100%;
        border-radius: 4px;
        font-weight: bold;
        border: 1px solid #333;
    }

    /* 선택 안 된 발판 */
    div[data-testid="stBaseButton-secondary"] button {
        background-color: #1a1c23;
        color: #555;
    }

    /* 파티원 이름 섹션 */
    .party-header {
        text-align: center;
        padding: 10px;
        font-size: 1.1rem;
        background-color: #111;
        border-bottom: 2px solid #333;
        margin-bottom: 15px;
    }
    
    /* 층 번호 스타일 */
    .floor-label {
        color: #888;
        font-size: 0.9rem;
        text-align: right;
        padding-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏰 로미오와 줄리엣 6단계")

# 상단 초기화 버튼
if st.button("🔄 모든 발판 초기화"):
    st.session_state.answers = [[0 for _ in range(4)] for _ in range(10)]
    st.rerun()

st.markdown("---")

# 파티원 이름 리스트 (이미지 참고)
party_names = ["1번", "2번", "3번", "4번"]
cols = st.columns(4)

for p_idx in range(4):
    with cols[p_idx]:
        # 파티원 이름 표시
        st.markdown(f"<div class='party-header'>{party_names[p_idx]}</div>", unsafe_allow_html=True)
        
        # 1층부터 10층까지 순서대로 생성
        for floor in range(10):
            # 층 번호와 4개 버튼을 한 행에 배치
            f_col1, f_col2 = st.columns([0.25, 1])
            
            with f_col1:
                st.markdown(f"<div class='floor-label'>{floor + 1}층</div>", unsafe_allow_html=True)
            
            with f_col2:
                p_cols = st.columns(4)
                for plate in range(1, 5):
                    with p_cols[plate-1]:
                        key = f"f{floor}_p{p_idx}_pl{plate}"
                        
                        # 상태 체크 로직
                        is_mine = (