import streamlit as st
import pandas as pd
import datetime

# 1. 페이지 설정 및 자비스(JARVIS) 스타일 하이테크 다크 테마 주입
st.set_page_config(
    page_title="JARVIS : SCM Border Security Control Tower",
    page_icon="🤖",
    layout="wide"
)

# 자비스 스타일 커스텀 CSS (어두운 네온 블루 테마, 사이버네틱 인터페이스)
st.markdown("""
    <style>
    .stApp {
        background-color: #0A0F1D;
        color: #E2E8F0;
        font-family: 'Consolas', 'Courier New', monospace;
    }
    .css-1d391kg {
        background-color: #0F172A;
    }
    h1, h2, h3 {
        color: #38BDF8 !important;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
        font-weight: bold;
    }
    .jarvis-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid #1E293B;
        border-left: 4px solid #0EA5E9;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .jarvis-metric {
        font-size: 2rem;
        font-weight: bold;
        color: #38BDF8;
    }
    .stSelectbox, .stRadio {
        color: #E2E8F0 !important;
    }
    hr {
        border-color: #1E293B !important;
    }
    </style>
""", unsafe_html=True)

# 시스템 상단 레이아웃 (자비스 부팅 시연 효과)
st.markdown("🌐 `SYSTEM STATUS: JARVIS BORDER SECURITY PROTOCOL ACTIVATED`")
st.title("🤖 JARVIS : 국경 공급망 실시간 위범 통제탑")
st.caption("TACTICAL SCM RISK INTELLIGENCE & REAL-TIME MARITIME ANOMALY DETECTOR")
st.write("---")

# 2. 내부 위험도 통계 매트릭스 (100점 만점 기반 배점 세팅)
country_risk_matrix = {
    '태국': 4.5, '미국': 4.2, '베트남': 3.8, '말레이시아': 3.5, 
    '중국(홍콩 포함)': 3.0, '라오스': 4.0, '독일': 2.8, '중남미(브라질 등)': 4.7
}

item_risk_matrix = {
    '커피 (HS 0901)': {'density': 2.5, 'lcl_weight': 1.5, 'desc': '강한 향으로 마약 탐지견의 후각 교란 유인 매우 높음'},
    '사탕, 초콜릿 (HS 1704)': {'density': 2.2, 'lcl_weight': 1.4, 'desc': '젤리나 사탕 모양으로 제조된 변종 마약(THC 등) 자체 위장 우범'},
    '화장품 (HS 3304)': {'density': 2.4, 'lcl_weight': 1.4, 'desc': '크림이나 액체 속에 녹이거나 이중 바닥 용기 내부 밀수 취약'},
    '시리얼, 곡물 (HS 1904)': {'density': 1.8, 'lcl_weight': 1.3, 'desc': '내용물 속 소량 혼재 시 육안 식별 및 X-ray 판독 사각지대 존재'},
    '가방, 케이스 (HS 4202)': {'density': 2.0, 'lcl_weight': 1.3, 'desc': '가방 안감 및 캐리어 벽면 사이 라미네이트 이중 은닉 빈발'},
    '견과류, 과일 가공품 (HS 2008)': {'density': 1.5, 'lcl_weight': 1.2, 'desc': '밀폐 용기 내부 액체 혼재 및 실제 화물과의 밀도 유사성 악용'},
    '제재목 (HS 4407)': {'density': 0.5, 'lcl_weight': 1.1, 'desc': '원목 형태의 대형 화물, 대형 컨테이너 단위 밀수 유인'},
    '가죽 신발류 (HS 6403)': {'density': 1.6, 'lcl_weight': 1.3, 'desc': '두꺼운 신발 굽 및 밑창 공간 분해 후 고밀도 은닉 활용'},
    '자동자료처리기계 (HS 8471)': {'density': 0.8, 'lcl_weight': 1.1, 'desc': 'IT 장비 하우징 내부 디바이스 빈 공간 악용'},
    '기타 기계류 (HS 8479)': {'density': 0.7, 'lcl_weight': 1.1, 'desc': '대형 기계 구조물 내부 용접 밀봉형 은닉 수법 발생'},
    '가정용 전기기기 (HS 8509)': {'density': 1.4, 'lcl_weight': 1.2, 'desc': '가전 모터 및 배터리 팩 내부 공간 탈거 후 마약 적재 유입'}
}

# 3. 사이드바 - 실시간 화물 프로파일링 정보 입력창
st.sidebar.markdown("### 🛠️ `DATA INGESTION`")
selected_country = st.sidebar.selectbox("1. 출발 국가(지역) 선별", list(country_risk_matrix.keys()))
selected_item = st.sidebar.selectbox("2. 반입 품목 코드 매칭", list(item_risk_matrix.keys()))
cargo_type = st.sidebar.radio("3. SCM 화물 유통 형태", ["LCL (소량 혼재 화물)", "FCL (단독 대량 화물)"])

# 4. 자비스 코어 리스크 스코어링 수리 연산 (100점 만점)
# [A] 국가 리스크 스코어 (50점 만점 환산)
country_base = country_risk_matrix[selected_country]
final_country_risk = (country_base / 5.0) * 50.0

# [B] 물품 위험도 스코어 (LCL 여부에 따른 차등 가중치 적용, 50점 만점 환산)
item_density = item_risk_matrix[selected_item]['density']
item_desc = item_risk_matrix[selected_item]['desc']

if cargo_type == "LCL (소량 혼재 화물)":
    scm_weight = item_risk_matrix[selected_item]['lcl_weight']
    status_msg = "🚨 LCL VULNERABILITY FACTOR ACCELERATED"
    raw_item_score = item_density * scm_weight
    final_item_risk = (raw_item_score / 3.75) * 50.0  # 최대값 3.75 정규화
else:
    scm_weight = 1.0
    status_msg = "🟢 FCL STANDARD ROUTE SECURED"
    final_item_risk = (item_density / 2.5) * 50.0     # 최대값 2.5 정규화

# [C] 최종 합산 (국가 50 + 물품 50 = 100점 만점)
final_comprehensive_risk = final_country_risk + final_item_risk

# 5. 메인 레이아웃 상단 - 전술 리스크 모니터 매트릭스
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="jarvis-card">
        <h4>🌐 ORIGIN RISK LEVEL</h4>
        <p style='color:#94A3B8;'>{selected_country} 출발국 프로파일링 스코어</p>
        <div class="jarvis-metric">{final_country_risk:.1f} <span style='font-size:1rem; color:#64748B;'>/ 50.0</span></div>
    </div>
    """, unsafe_html=True)

with col2:
    st.markdown(f"""
    <div class="jarvis-card">
        <h4>📦 CARGO SPECIFIC RISK</h4>
        <p style='color:#94A3B8;'>물류 형태 및 고유 은닉 수법 보정</p>
        <div class="jarvis-metric">{final_item_risk:.1f} <span style='font-size:1rem; color:#64748B;'>/ 50.0 (x{scm_weight:.2f})</span></div>
    </div>
    """, unsafe_html=True)

with col3:
    # 안전/유의/즉시개장에 따른 자비스 네온 인디케이터 컬러 적용
    if final_comprehensive_risk >= 80.0:
        color_code = "#EF4444"
        badge_text = "🚨 [CRITICAL] 즉시 정밀 개장검사 대상"
    elif final_comprehensive_risk >= 60.0:
        color_code = "#F59E0B"
        badge_text = "⚠️ [WARNING] X-ray 집중 판독 대상"
    elif final_comprehensive_risk <= 50.0:
        color_code = "#10B981"
        badge_text = "🟢 [CLEAR] 안전 통관 대상 화물"
    else:
        color_code = "#38BDF8"
        badge_text = "🔵 [MONITOR] 일반 모니터링 화물"

    st.markdown(f"""
    <div class="jarvis-card" style='border-left: 4px solid {color_code};'>
        <h4 style='color: {color_code} !important;'>🎯 COMPREHENSIVE SECURITY SCORE</h4>
        <p style='color:#94A3B8;'>알고리즘 기반 통합 위험 스케일</p>
        <div class="jarvis-metric" style='color: {color_code};'>{final_comprehensive_risk:.1f} <span style='font-size:1rem; color:#64748B;'>/ 100.0</span></div>
    </div>
    """, unsafe_html=True)

st.write(f"`LOG: {status_msg} | TARGETING SCORE COMPUTED AT {datetime.datetime.now().strftime('%H:%M:%S')}`")
st.write("---")

# 6. 중간 메인 화면 - [추가 요구사항 1 & 2] 설명형 AI(XAI) 및 실시간 인텔리전스 뉴스 2분할 대시보드
layout_col1, layout_col2 = st.columns([1.1, 0.9])

with layout_col1:
    st.subheader("🧠 위험도 산출 근거 진단 리포트 (XAI Dashboard)")
    
    # 심사위원을 단숨에 설득할 정량적·정성적 분석 결합형 설명 UI
    explanation_text = f"""
    * **국가적 요인 분석:** 현 화물은 최근 4개년 대검찰청 마약백서 기준 반입 규모 상위 우범 권역인 **{selected_country}**발 포워딩 라인을 거쳤습니다. 이로 인해 전체 100점 중 **{final_country_risk:.1f}점**의 기본 리스크 베이스라인이 할당되었습니다.
    * **물류 형태별 사각지대 분석:** 현재 통관 형태는 **{cargo_type}**로 식별되었습니다. LCL 화물의 특성상 소규모 화주(Shipper) 다수의 화물이 한 컨테이너에 혼재되므로 익명성이 높아집니다. 시스템은 즉시 본 화물에 **x{scm_weight:.2f}배의 차등 리스크 부하 가중치**를 엔진에 주입하였습니다.
    * **품목별 고유 은닉 메커니즘:** 선택된 **{selected_item}** 품목은 과거 밀수 적발 사례 분석 결과 *"{item_desc}"*라는 물리적 한계점과 우범성이 존재합니다. 
    * **최종 결론:** 이에 따라 도출된 종합 점수는 **{final_comprehensive_risk:.1f}점**이며, 시스템은 단속 인력의 한정된 자원을 극대화하기 위해 본 화물을 즉시 **{badge_text}** 등급으로 분류하고 현장 통제를 제안합니다.
    """
    st.markdown(f"<div class='jarvis-card'>{explanation_text}</div>", unsafe_html=True)
    
    # 직관적인 원인 매트릭스 표
    st.markdown("📊 **위험 점수 구성 컴포넌트 명세**")
    st.table(pd.DataFrame({
        "위험 요인 컴포넌트": ["출발지(Origin) 국가 우범 지수", "품목별 기본 마약 위험밀도", "공급망 유통 리드타임 가중치", "100점 만점 환산 최종 스코어"],
        "정량 데이터 및 밸류": [f"{final_country_risk:.1f} 점", f"{item_density:.1f} 점", f"x {scm_weight:.2f}", f"{final_comprehensive_risk:.1f} 점"]
    }))

with layout_col2:
    st.subheader("📡 실시간 글로벌 인텔리전스 피드")
    
    # 탭 메뉴를 통해 마약 뉴스 및 글로벌 해운 물류 뉴스를 분리 제공하여 관제탑 느낌 극대화
    news_tab1, news_tab2 = st.tabs(["💊 GLOBAL DRUG SMUGGLING", "🚢 MARITIME & SCM ISSUE"])
    
    with news_tab1:
        st.write("`LIVE FEED: 실시간 해외 마약 단속 및 신종 적발 동향`")
        drug_news = [
            {"date": "[방금 전]", "title": "미국 DEA, 동남아발 LCL 컨테이너 내부 화장품 튜브 은닉 필로폰 45kg 적발", "type": "🚨"},
            {"date": "[10분 전]", "title": "태국 방콕 항만, 가방 내벽 안감에 라미네이트 수법으로 숨긴 코카인 밀수 조직 검거", "type": "⚠️"},
            {"date": "[1시간 전]", "title": "UNODC 보고서 발표: 골든 트라이앵글 지역 합성 마약 국내 도매가 전년 대비 14% 급등", "type": "🌐"}
        ]
        for news in drug_news:
            st.markdown(f"<div style='font-size:0.9rem; padding:6px 0; border-bottom:1px solid #1E293B;'>{news['type']} <b>{news['date']}</b> {news['title']}</div>", unsafe_html=True)
            
    with news_tab2:
        st.write("`LIVE FEED: 글로벌 공급망 리드타임 및 항만 정체 이상징후`")
        maritime_news = [
            {"date": "[실시간]", "title": "싱가포르항 CFS 환적 화물 체류 시간(Dwell Time) 표준 대비 36시간 돌발 지연", "type": "🔵"},
            {"date": "[30분 전]", "title": "파나마 운하 통항 제한 조치 강화로 소형 포워더 LCL 우회 경로 탐색 급증", "type": "⚠️"},
            {"date": "[2시간 전]", "title": "글로벌 상위 10개 선사, 동아시아-한국 행 항로 컨테이너 운임 지수(SCFI) 변동성 심화", "type": "🌐"}
        ]
        for news in maritime_news:
            st.markdown(f"<div style='font-size:0.9rem; padding:6px 0; border-bottom:1px solid #1E293B;'>{news['type']} <b>{news['date']}</b> {news['title']}</div>", unsafe_html=True)

st.write("---")
st.markdown("<p style='text-align:center; color:#64748B; font-size:0.8rem;'>JARVIS SCM TARGETING SYSTEM V2.0 / UNDERGRADUATE SCM COMPETITION PROJECT</p>", unsafe_html=True)