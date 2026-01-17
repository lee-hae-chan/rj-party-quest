import streamlit as st

# 페이지 설정
st.set_page_config(page_title="로미오와 줄리엣 6단계 도우미", layout="wide")

# 세션 상태 초기화
if 'answers' not in st.session_state:
    st.session_state.answers = [[0 for _ in range(4)] for _ in range(10)]

# --- CSS 스타일 ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    
    /* 버튼 기본 스타일 */
    .stButton button {
        height: 40px;
        width: 100%;
        border-radius: 4px;
        font-weight: bold;
        border: 1px solid #333;
    }

    /* 비활성화(disabled)된 버튼 스타일 - 다른 사람이 고른 경우 */
    .stButton button:disabled {
        background-color: #1a1c23 !important;
        color: #ff4b4b !important; 
        border: 1px solid #444 !important;
        cursor: not-allowed;
    }

    .party-header {
        text-align: center;
        padding: 10px;
        font-size: 1.1rem;
        background-color: #111;
        border-bottom: 2px solid #333;
        margin-bottom: 15px;
    }
    
    .floor-label {
        color: #888;
        font-size: 0.9rem;
        text-align: right;
        padding-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏰 로미오와 줄리엣 6단계 도우미")

if st.button("🔄 모든 발판 초기화"):
    st.session_state.answers = [[0 for _ in range(4)] for _ in range(10)]
    st.rerun()

st.markdown("---")

# 요청하신 대로 파티원 이름을 변경했습니다.
party_names = ["1번", "2번", "3번", "4번"]
cols = st.columns(4)

for p_idx in range(4):
    with cols[p_idx]:
        st.markdown(f"<div class='party-header'>{party_names[p_idx]}</div>", unsafe_allow_html=True)
        
        # 1층부터 10층까지 순서대로
        for floor in range(10):
            f_col1, f_col2 = st.columns([0.25, 1])
            
            with f_col1:
                st.markdown(f"<div class='floor-label'>{floor + 1}층</div>", unsafe_allow_html=True)
            
            with f_col2:
                p_cols = st.columns(4)
                for plate in range(1, 5):
                    with p_cols[plate-1]:
                        key = f"f{floor}_p{p_idx}_pl{plate}"
                        
                        # 1. 내가 선택한 것인지 확인
                        is_mine = (st.session_state.answers[floor][p_idx] == plate)
                        
                        # 2. 다른 사람이 이미 이 번호를 선택했는지 확인
                        is_taken_by_others = False
                        for other_p in range(4):
                            if other_p != p_idx and st.session_state.answers[floor][other_p] == plate:
                                is_taken_by_others = True
                                break
                        
                        # 버튼 상태 설정
                        if is_mine:
                            b_label = str(plate)
                            b_type = "primary"
                            b_disabled = False
                        elif is_taken_by_others:
                            b_label = str(plate) 
                            b_type = "secondary"
                            b_disabled = True   # 다른 사람이 골랐으므로 클릭 불가
                        else:
                            b_label = " "
                            b_type = "secondary"
                            b_disabled = False

                        if st.button(b_label, key=key, type=b_type, disabled=b_disabled, use_container_width=True):
                            if is_mine:
                                st.session_state.answers[floor][p_idx] = 0
                            else:
                                st.session_state.answers[floor][p_idx] = plate
                            st.rerun()