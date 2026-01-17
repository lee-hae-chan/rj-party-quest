import streamlit as st

# 페이지 설정
st.set_page_config(page_title="로미오와 줄리엣 6단계 도우미", layout="wide")

# 세션 상태 초기화
if 'answers' not in st.session_state:
    # answers[층][파티원] = 정답 발판 번호 (0~9층, 0은 미선택)
    st.session_state.answers = [[0 for _ in range(4)] for _ in range(10)]

# --- CSS 스타일 (이미지 느낌 구현) ---
st.markdown("""
<style>
    /* 전체 배경 및 폰트 */
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    
    /* 버튼 기본 스타일 */
    .stButton button {
        height: 45px;
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s;
        border: 1px solid #333;
    }

    /* 선택되지 않은 빈 발판 (검정/어두운 회색) */
    div[data-testid="stBaseButton-secondary"] button {
        background-color: #1a1c23;
        color: #444;
    }

    /* 다른 사람이 선택한 발판 (빨간색 텍스트 또는 테두리 - 이미지의 2번 발판 느낌) */
    /* Streamlit 기본 버튼으로는 한계가 있어 로직으로 처리 */

    /* 층 구분선 및 레이아웃 */
    .floor-container {
        border: 1px solid #333;
        padding: 10px;
        border-radius: 10px;
        background-color: #000000;
        text-align: center;
    }
    
    .party-name {
        text-align: center;
        padding: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        background-color: #111;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏰 로미오와 줄리엣 6단계 도우미")

# 상단 컨트롤러
col_ctrl1, col_ctrl2 = st.columns([1, 5])
with col_ctrl1:
    if st.button("🔄 전체 초기화"):
        st.session_state.answers = [[0 for _ in range(4)] for _ in range(10)]
        st.rerun()

# --- 메인 보드 구성 ---
# 이미지처럼 파티원별로 4개의 큰 구역(Column)을 나눕니다.
party_names = ["1번", "2번", "3번", "4번"] # 이미지 예시 이름
cols = st.columns(4)

for p_idx in range(4):
    with cols[p_idx]:
        # 파티원 이름 헤더
        st.markdown(f"<div class='party-name'>{party_names[p_idx]}</div>", unsafe_allow_html=True)
        
        # 층을 이미지처럼 10층(위) -> 1층(아래) 순서로 렌더링
        for floor in range(9, -1, -1):
            f_col1, f_col2 = st.columns([0.3, 1])
            
            with f_col1:
                st.markdown(f"<div style='margin-top:10px;'>{floor + 1}층</div>", unsafe_allow_html=True)
            
            with f_col2:
                # 4개의 발판을 한 줄에 배치
                p_cols = st.columns(4)
                for plate in range(1, 5):
                    with p_cols[plate-1]:
                        key = f"f{floor}_p{p_idx}_pl{plate}"
                        
                        # 상태 확인
                        is_mine = (st.session_state.answers[floor][p_idx] == plate)
                        
                        # 다른 파티원이 해당 층의 이 발판을 선택했는지 확인
                        others_selected = False
                        for other_p in range(4):
                            if other_p != p_idx and st.session_state.answers[floor][other_p] == plate:
                                others_selected = True
                                break
                        
                        # 버튼 스타일 결정
                        if is_mine:
                            # 내가 선택한 정답 (파란색)
                            b_type = "primary"
                            label = f"{plate}"
                        elif others_selected:
                            # 남이 선택한 것 (이미지의 빨간색 숫자 느낌)
                            # Streamlit은 버튼별 개별 색상 지정이 까다로워 일반 버튼으로 표시하되 로직만 분리
                            b_type = "secondary"
                            label = f"{plate}" # 이미지는 빨간색 숫자로 표시됨
                        else:
                            # 아무도 안 고름 (빈 칸)
                            b_type = "secondary"
                            label = " "

                        if st.button(label, key=key, type=b_type, use_container_width=True):
                            if is_mine:
                                st.session_state.answers[floor][p_idx] = 0
                            else:
                                st.session_state.answers[floor][p_idx] = plate
                            st.rerun()