import streamlit as st
import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup
import urllib.parse
import numpy as np
import time  # ⏳ 1초 로딩 지연을 위한 라이브러리 인입

# ====================================================================
# 1. 페이지 레이아웃 및 국경관제실 전용 프리미엄 미드나잇 다크 CSS
# ====================================================================
st.set_page_config(
    page_title="JANG BOGO : INU SCM Border Security",
    page_icon="⚓",
    layout="wide"
)

# 보안 관제실 전용 프리미엄 다크 테마 디자인 스킨 적용
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght=400;600;700&display=swap');
    
    .stApp {
        background-color: #0B132B !important;
        font-family: 'Pretendard', sans-serif;
    }
    
    html, body, [class*="css"] {
        color: #E2E8F0 !important;
    }
    
    /* 퓨어 다크 글래스모피즘 카드 UI */
    .toss-card {
        background-color: #1C2541;
        padding: 32px;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        margin-bottom: 24px;
        border: 1px solid #3A506B;
    }
    
    .toss-title {
        font-size: 22px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 18px;
        letter-spacing: -0.3px;
        border-left: 4px solid #48CAE4;
        padding-left: 10px;
    }
    
    [data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1F2937;
    }
    
    /* 사이드바 Form 내부 입력창 시인성 커스텀 */
    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }
    
    .stSelectbox div, .stNumberInput div, .stRadio div {
        background-color: #1F2937 !important;
        color: #FFFFFF !important;
    }
    input {
        color: #FFFFFF !important;
        background-color: #1F2937 !important;
        font-weight: 600 !important;
        border: 1px solid #48CAE4 !important;
    }
    label p {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
    }
    
    /* 🔥 [버튼 커스텀] 확인 버튼을 관제실 스타일의 와이드한 블루 버튼으로 변경 */
    .stButton > button {
        width: 100% !important;
        background-color: #48CAE4 !important;
        color: #0B132B !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 0px !important;
        font-size: 16px !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #00B4D8 !important;
        box-shadow: 0 0 15px rgba(72, 202, 228, 0.6) !important;
        color: #0B132B !important;
    }
    
    /* 커스텀 다크 테이블 CSS */
    .custom-dark-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
        background-color: #111827;
        border-radius: 12px;
        overflow: hidden;
    }
    .custom-dark-table th {
        background-color: #1F2937;
        color: #48CAE4;
        text-align: left;
        padding: 12px;
        font-size: 14px;
        font-weight: 700;
        border-bottom: 2px solid #3A506B;
    }
    .custom-dark-table td {
        padding: 12px;
        color: #E2E8F0;
        font-size: 14px;
        border-bottom: 1px solid #1C2541;
    }
    </style>
    """, unsafe_allow_html=True)


# ====================================================================
# 📊 [백엔드 데이터 엔진] 단일 엑셀 파일(.xlsx)의 다중 시트 파싱 및 수리 계산
# ====================================================================
@st.cache_data
def load_and_compile_master_engine():
    excel_file = '2022-2025년 마약 분기별 통계.xlsx'
    
    df_country = pd.read_excel(excel_file, sheet_name='국가별_분기별_통계_통합')
    df_item = pd.read_excel(excel_file, sheet_name='품목가중치근거')
    
    years = ['2022', '2023', '2024', '2025']
    weights = {'2022': 1.0, '2023': 1.2, '2024': 1.2, '2025': 1.5}
    quarters = ['1Q', '2Q', '3Q', '4Q']
    
    total_row = df_country[df_country['국가(지역)'] == '합계'].iloc[0]
    total_stats = {}
    for y in years:
        total_stats[y] = {
            'cases': sum([float(total_row[f'{y}년 {q} 건수']) for q in quarters]),
            'weight': sum([float(total_row[f'{y}년 {q} 중량(kg)']) for q in quarters])
        }
        
    country_risk_matrix = {}
    for _, row in df_country.iloc[:8].iterrows():
        c_name = row['국가(지역)']
        total_risk = 0
        for y in years:
            c_cases = sum([float(row[f'{y}년 {q} 건수']) for q in quarters])
            c_weight = sum([float(row[f'{y}년 {q} 중량(kg)']) for q in quarters])
            
            freq = (c_cases / total_stats[y]['cases']) * 100 if total_stats[y]['cases'] > 0 else 0
            severity = (c_weight / total_stats[y]['weight']) * 100 if total_stats[y]['weight'] > 0 else 0
            
            y_risk = (freq * 0.4 * weights[y]) + (severity * 0.6 * weights[y])
            total_risk += y_risk
            
        country_risk_matrix[c_name] = round(total_risk, 2)
        
    item_risk_matrix = {}
    for _, row in df_item.iterrows():
        raw_weight_value = float(row['품목 가중치'])
        item_risk_matrix[row['품목명']] = {
            'weight': raw_weight_value,
            'calculated_risk': raw_weight_value * 25.0,
            'desc': row['은닉 특성 및 위험 근거']
        }
        
    return country_risk_matrix, item_risk_matrix, weights

try:
    country_risk_matrix, item_risk_matrix, year_weights = load_and_compile_master_engine()
except Exception as e:
    st.error(f"⚠️ 데이터 파일 연동 실패: {e}. 작업 환경 내 파일 구성을 확인하세요.")
    st.stop()


def scan_realtime_global_issue(country_name):
    query = f"{country_name} 마약 밀수"
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    feeds = []
    try:
        response = requests.get(url, timeout=3)
        soup = BeautifulSoup(response.text, 'xml')
        items = soup.find_all('item')[:3]
        for item in items:
            title = item.title.text
            clean_title = title.split(" - ")[0] if " - " in title else title
            feeds.append({"title": clean_title, "link": item.link.text})
        return feeds
    except:
        return []


# ====================================================================
# 2. 상단 헤더 브랜딩
# ====================================================================
st.markdown("""
    <div style='padding: 8px 0px 16px 0px;'>
        <div style='color: #48CAE4; font-size: 13px; font-weight: 700; letter-spacing: 1.5px; margin-bottom: 6px;'>🛡️ KCS CUSTOMS BORDER PROTECTION AI / NIGHT WATCH MODE</div>
        <h1 style='font-size: 40px; font-weight: 800; color: #FFFFFF; margin: 0; letter-spacing: -0.5px;'>장보고 스코어링 모델 <span style='font-size: 26px; color: #94A3B8; font-weight: 500;'>JANG BOGO</span></h1>
        <div style='font-size: 15px; color: #CBD5E1; font-weight: 600; margin-top: 4px;'>Incheon National University | Supply Chain Security Lab</div>
    </div>
    """, unsafe_allow_html=True)
st.write("---")


# ====================================================================
# 3. 사이드바 - [제안 반영] 버튼 동기화를 위한 Form 인터페이스 감싸기
# ====================================================================
st.sidebar.markdown("<h3 style='color:#FFFFFF; font-weight:700; margin-bottom:12px;'>📋 통관 화물 프로파일</h3>", unsafe_allow_html=True)

# st.sidebar.form을 선언하여 사용자가 모든 입력을 마친 후 버튼을 눌렀을 때만 작동하도록 가둡니다.
with st.sidebar.form(key='security_panel'):
    selected_country = st.selectbox("🌐 출발 국가(Origin) 선택", list(country_risk_matrix.keys()))
    selected_item = st.selectbox("📦 반입 품목(Item Classification)", list(item_risk_matrix.keys()))
    cargo_weight = st.number_input("⚖️ 화물 실중량 입력 (kg)", min_value=1.0, value=2000.0, step=100.0)
    cargo_type = st.radio("🚢 유통 형태 선택", ["LCL (소량 혼재 화물)", "FCL (단독 대량 화물)"])
    
    # 맨 밑에 배치되는 확인(제출) 버튼
    submit_button = st.form_submit_submit_button(label='🔍 국경 보안 스캔 실행')


# ====================================================================
# 4. [확인 및 로딩 메커니즘 가동] 
# ====================================================================
# 사용자가 버튼을 누르면 1초간 로딩을 띄운 뒤 연산 결과를 보여줍니다.
if submit_button:
    with st.spinner("🔒 통합 물류 공급망 및 실시간 동적 국경 인텔리전스 위협 요소를 정밀 스캔 중..."):
        time.sleep(1.0) # ⏳ 요청하신 대기 시간 1초 부여
else:
    # 앱이 처음 켜졌거나 입력을 바꾼 뒤 아직 버튼을 누르지 않은 상태 알림
    st.info("💡 사이드바 패널에서 프로파일 정보를 입력 또는 변경하신 후, 하단의 [🔍 국경 보안 스캔 실행] 버튼을 눌러주세요.")
    st.stop()


# ====================================================================
# 5. [장보고 핵심 엔진] 품목 분류별 중량 이중성 동적 수식 연산 (보안 검사 승인 후 가동)
# ====================================================================
raw_country_risk = country_risk_matrix[selected_country]

item_w = item_risk_matrix[selected_item]['weight']
item_desc = item_risk_matrix[selected_item]['desc']
base_excel_item_risk = item_risk_matrix[selected_item]['calculated_risk']

# 품목 카테고리 정의 (벌크형 대형 화물 vs 일상 소비재 위장 화물)
high_bulk_items = ["목재", "특수 기계류", "컴퓨터, 자재", "가전제품"]

if selected_item in high_bulk_items:
    weight_factor = np.log10(cargo_weight + 1) / np.log10(2001)
    dynamic_item_risk = base_excel_item_risk * weight_factor
    weight_logic_desc = f"벌크형 고중량 가중 연동 (지수 비율: {weight_factor:.2f}배)"
else:
    if cargo_weight < 500:
        dynamic_item_risk = base_excel_item_risk * 1.3
        weight_logic_desc = "소비재 우회용 소량 쪼개기 밀수 패널티 적용 (+30%)"
    else:
        dynamic_item_risk = base_excel_item_risk * 0.85
        weight_logic_desc = "소비재 대형 정상 화물 위험도 감쇄 적용 (-15%)"

# 유통 형태(LCL) 결합 조건
if cargo_type == "LCL (소량 혼재 화물)":
    calculated_item_risk = dynamic_item_risk * item_w
    lcl_penalty_status = f"가동 중 (품목 가중치 {item_w}배 추가 승산)"
else:
    calculated_item_risk = dynamic_item_risk
    lcl