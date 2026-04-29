import pandas as pd
import streamlit as st

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="JANG BOGO: Logistics Risk System", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #00050a; color: #00d4ff; }
    .stApp { background-color: #00050a; }
    label { color: #00d4ff !important; font-weight: bold; }
    .result-box { 
        background-color: #001a33; 
        border: 2px solid #00d4ff; 
        padding: 50px; 
        border-radius: 20px; 
        text-align: center;
        box-shadow: 0 0 40px #0055ff;
        margin-top: 20px;
    }
    .score-text { 
        font-size: 140px !important; 
        color: #00ffcc; 
        text-shadow: 0 0 25px #00ffcc; 
        margin: 10px 0;
        font-family: 'Impact', sans-serif;
    }
    hr { border: 1px solid #0055ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. 장보고 엔진 (사용자 조건 반영: 파일명 소문자, 시트명 대문자)
@st.cache_data
def build_jangbogo_engine():
    try:
        # 파일명은 소문자 'data.xlsx', 시트명은 대문자 'COUNTRY', 'ITEM'
        country_df = pd.read_excel('data.xlsx', sheet_name='COUNTRY')
        item_df = pd.read_excel('data.xlsx', sheet_name='ITEM')
        
        # 모든 경우의 수 생성 (Cross Join)
        country_df['key'] = 1
        item_df['key'] = 1
        total_df = pd.merge(country_df, item_df, on='key').drop('key', axis=1)
        
        # 4:6 가중치 적용 (국가 0.4 : 물품 0.6)
        total_df['raw_score'] = (total_df['국가점수'] * 0.4) + (total_df['물품점수'] * 0.6)
        
        # 전체 조합 내 상대적 백분위 환산 (100점 만점)
        total_df['final_score'] = total_df['raw_score'].rank(pct=True) * 100
        
        return total_df, country_df['국가명'].unique(), item_df['HS코드'].unique()
    except Exception as e:
        # 에러 메시지를 화면에 구체적으로 표시
        st.error(f"데이터 로드 실패: {e}")
        st.info("💡 확인사항: 파일명이 'data.xlsx'이고 시트명이 'COUNTRY', 'ITEM'인지 확인해주세요.")
        return None, None, None

# 엔진 구동
total_model, country_list, item_list = build_jangbogo_engine()

# 3. 사용자 인터페이스
if total_model is not None:
    st.markdown("<h1 style='text-align: center; color: #00d4ff; letter-spacing: 10px;'>⚓ JANG BOGO: ANOMALY DETECTION</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #58a6ff;'>Incheon National Univ. Logistics Intelligence Model</p>", unsafe_allow_html=True)
    st.write("---")

    col1, col2 = st.columns(2)
    with col1:
        selected_country = st.selectbox("출발 국가(ORIGIN)", country_list)
    with col2:
        selected_item = st.selectbox("품목(HS-CODE)", item_list)

    # 선택된 값에 따른 결과 추출
    result_data = total_model[
        (total_model['국가명'] == selected_country) & 
        (total_model['HS코드'] == selected_item)
    ].iloc[0]

    final_score = result_data['final_score']

    # 4. 결과 출력
    st.write("")
    st.write(">> 데이터 분석 엔진 가동 중...")
    
    st.markdown(f"""
        <div class="result-box">
            <p style="color: #00d4ff; font-size: 26px; letter-spacing: 3px;">종합 위험 지수 (RISK INDEX)</p>
            <p class="score-text">{final_score:.1f}%</p>
            <p style="color: #58a6ff; font-size: 18px;">전체 화물 조합 대비 상대적 위험 수준</p>
        </div>
    """, unsafe_allow_html=True)

    # 5. 위험도 알림
    st.write("---")
    if final_score >= 85:
        st.error(f"🚨 [경보] 고위험 화물 감지: 상위 {100-final_score:.1f}% 내에 있는 우범군입니다. 즉시 개장 검사를 권고합니다.")
    elif final_score >= 50:
        st.warning(f"⚠️ [주의] 중점 관리 대상: 평균 위험 수치를 상회합니다. 선별 검사를 권장합니다.")
    else:
        st.success(f"✅ [안전] 저위험 화물: 신속 통관 프로세스 유지가 가능합니다.")