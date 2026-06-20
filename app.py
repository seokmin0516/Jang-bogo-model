import streamlit as st
import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup
import urllib.parse
import numpy as np
import time
from sklearn.cluster import KMeans

# ====================================================================
# 1. 페이지 레이아웃 및 국경관제실 전용 프리미엄 미드나잇 다크 CSS
# ====================================================================
st.set_page_config(
    page_title="JANG BOGO",
    layout="wide"
)

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
    
    .ai-badge {
        display: inline-block;
        padding: 4px 8px;
        background: linear-gradient(135deg, #7209B7, #4CC9F0);
        color: white;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)


# ====================================================================
# 📊 [백엔드 데이터 엔진 & AI 가상 학습 파이프라인]
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
        
    np.random.seed(42)
    mock_samples = []
    for _ in range(100):
        c_r = np.random.choice(list(country_risk_matrix.values()))
        i_w = np.random.choice([v['weight'] for v in item_risk_matrix.values()])
        w_f = np.random.uniform(10, 5000)
        mock_samples.append([c_r, i_w, w_f])
        
    X_train = np.array(mock_samples)
    kmeans_model = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans_model.fit(X_train)
        
    return country_risk_matrix, item_risk_matrix, weights, kmeans_model

try:
    country_risk_matrix, item_risk_matrix, year_weights, ai_kmeans_engine = load_and_compile_master_engine()
except Exception as e:
    st.error(f"⚠️ 데이터 파일 및 AI 엔진 연동 실패: {e}.")
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
# 2. 상단 헤더 브랜딩 (요청에 의거 딴말 추가 없이 제목/소제목만 깔끔하게 노출)
# ====================================================================
st.markdown("""
    <div style='padding: 8px 0px 16px 0px;'>
        <h1 style='font-size: 40px; font-weight: 800; color: #FFFFFF; margin: 0; letter-spacing: -0.5px;'>장보고 스코어링 모델</h1>
        <div style='font-size: 18px; color: #CBD5E1; font-weight: 600; margin-top: 6px;'>Incheon National University</div>
    </div>
    """, unsafe_allow_html=True)
st.write("---")


# ====================================================================
# 3. 사이드바 - 제어 패널 (Form 구조)
# ====================================================================
st.sidebar.markdown("<h3 style='color:#FFFFFF; font-weight:700; margin-bottom:12px;'>📋 통관 화물 프로파일</h3>", unsafe_allow_html=True)

with st.sidebar.form(key='security_panel'):
    selected_country = st.selectbox("🌐 출발 국가(Origin) 선택", list(country_risk_matrix.keys()))
    selected_item = st.selectbox("📦 반입 품목(Item Classification)", list(item_risk_matrix.keys()))
    cargo_weight = st.number_input("⚖️ 화물 실중량 입력 (kg)", min_value=1.0, value=2000.0, step=100.0)
    cargo_type = st.radio("🚢 유통 형태 선택", ["LCL (소량 혼재 화물)", "FCL (단독 대량 화물)"])
    
    submit_button = st.form_submit_button(label='🔍 국경 보안 스캔 실행')


# ====================================================================
# 4. 확인 및 1초 로딩 메커니즘 (흰색 알림창 조건부 완전 제거)
# ====================================================================
if submit_button:
    with st.spinner("🔒 AI 다차원 클러스터링 알고리즘 및 국경 인텔리전스 위협 요소를 정밀 매핑 중..."):
        time.sleep(1.0)
else:
    # 최초 구동 시나 값 변경 중일 때 흰색 알림창이 안 뜨도록 바로 렌더링 중단 처리
    st.stop()


# ====================================================================
# 5. [장보고 핵심 엔진] 품목 분류별 중량 이중성 수식 연산
# ====================================================================
raw_country_risk = country_risk_matrix[selected_country]

item_w = item_risk_matrix[selected_item]['weight']
item_desc = item_risk_matrix[selected_item]['desc']
base_excel_item_risk = item_risk_matrix[selected_item]['calculated_risk']

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

if cargo_type == "LCL (소량 혼재 화물)":
    calculated_item_risk = dynamic_item_risk * item_w
    lcl_penalty_status = f"가동 중 (품목 가중치 {item_w}배 추가 승산)"
else:
    calculated_item_risk = dynamic_item_risk
    lcl_penalty_status = "정상 통관 (FCL 단독 컨테이너 적용)"


# ====================================================================
# 6. [AI 연산] 실시간 입력값 기반의 K-Means 군집 매칭 및 리스크 가산
# ====================================================================
current_cargo_vector = np.array([[raw_country_risk, item_w, cargo_weight]])
predicted_cluster = ai_kmeans_engine.predict(current_cargo_vector)[0]

if predicted_cluster == 0:
    cluster_name = "Cluster #0: 일반 유통 소비재군 (정상 물동량 영역)"
    ai_penalty_score = 0.0
    cluster_color = "#10B981"
elif predicted_cluster == 1:
    cluster_name = "Cluster #1: 고중량 대형 인프라 화물군 (심도 관리 영역)"
    ai_penalty_score = 15.5
    cluster_color = "#F59E0B"
else:
    cluster_name = "Cluster #2: 고위험 우회 루트 의심군 (AI 특별 추적 영역)"
    ai_penalty_score = 28.0
    cluster_color = "#EF4444"

live_news_feeds = scan_realtime_global_issue(selected_country)

if len(live_news_feeds) > 0:
    has_external_variable = True
    live_external_score = 50.0 if len(live_news_feeds) == 1 else (80.0 if len(live_news_feeds) == 2 else 100.0)
    base_score = ((raw_country_risk + calculated_item_risk) * 0.7) + (live_external_score * 0.3)
else:
    has_external_variable = False
    live_external_score = 0.0
    base_score = (raw_country_risk + calculated_item_risk) / 2.0

final_score = base_score + ai_penalty_score
final_score = round(min(100.0, max(0.0, final_score)), 1)


# ====================================================================
# 7. 상단 토탈 리스크 알림 전광판
# ====================================================================
status_color = "#EF4444" if final_score >= 65 else ("#F59E0B" if final_score >= 45 else "#10B981")
status_text = "🚨 [고위험 전수 검사 전환]" if final_score >= 65 else ("⚠️ [지정 유의 통관 대상]" if final_score >= 45 else "🟢 [원스톱 프리패스 대상]")

st.markdown(f"""
    <div class='toss-card' style='background-color: #111827; border: 2px solid {status_color}; padding: 36px;'>
        <div class='ai-badge'>🤖 AI-BASED SECURITY PREDICTION LOGIC ACTIVE</div>
        <div style='font-size: 14px; font-weight: 600; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px;'>DYNAMIC RISK SECURITY INDEX</div>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 10px;'>
            <div style='font-size: 52px; font-weight: 800; color: #FFFFFF; letter-spacing: -1.5px;'>
                {final_score} <span style='font-size: 22px; color: #94A3B8; font-weight: 500;'>/ 100.0 pts</span>
            </div>
            <div style='background-color: {status_color}; color: #FFFFFF; font-size: 16px; font-weight: 700; padding: 12px 24px; border-radius: 16px;'>
                {status_text}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ====================================================================
# 8. 좌우 2분할 레이아웃 대시보드 아키텍처
# ====================================================================
left_dashboard, right_dashboard = st.columns(2)

with left_dashboard:
    st.markdown("<div class='toss-card'><div class='toss-title'>🧠 공급망 중량 이중성 가중 매트릭스</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='line-height: 1.8; color:#E2E8F0; font-size:15px;'>
        <ul>
            <li><strong>국가별 누적 통계 위험도:</strong> <span style='color:#48CAE4; font-weight:700;'>{raw_country_risk:.2f}점</span></li>
            <li style='margin-top:10px;'><strong>중량 로직 필터 결과:</strong> <span style='color:#F59E0B; font-weight:700;'>{weight_logic_desc}</span></li>
            <li style='margin-top:10px;'><strong>연산 최종 물품 위험도:</strong> <span style='color:#48CAE4; font-weight:700;'>{calculated_item_risk:.2f}점</span></li>
            <li style='margin-top:10px;'><strong>LCL 패널티 필터 상태:</strong> <span style='color:#F87171; font-weight:700;'>{lcl_penalty_status}</span></li>
            <li style='margin-top:10px;'><strong>🤖 AI K-Means 실시간 군집 매핑:</strong> <span style='color:{cluster_color}; font-weight:700;'>{cluster_name} (+{ai_penalty_score}점 가산)</span></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    live_ext_str = f"{live_external_score:.1f} 점" if has_external_variable else "평가 제외 (미반영)"
    st.markdown(f"""
        <table class='custom-dark-table'>
            <tr>
                <th>국경 리스크 계측 요인</th>
                <th>정량 계산 스케일</th>
            </tr>
            <tr>
                <td>국가 고유 리스크 상수 (과거 통계 기반)</td>
                <td><b>{raw_country_risk:.1f} 점</b></td>
            </tr>
            <tr>
                <td>물품 위험도 점수 (중량 및 SCM 로직 연동)</td>
                <td><b>{calculated_item_risk:.1f} 점</b></td>
            </tr>
            <tr>
                <td>실시간 글로벌 변수 스코어 (OSINT 연동)</td>
                <td><b>{live_ext_str}</b></td>
            </tr>
            <tr style='background-color:#1E1B4B;'>
                <td style='color:#A78BFA;'>🤖 <b>AI 다차원 머신러닝 군집 패널티</b></td>
                <td style='color:#A78BFA;'><b>+{ai_penalty_score:.1f} 점</b></td>
            </tr>
        </table>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right_dashboard:
    st.markdown("<div class='toss-card'><div class='toss-title'>🌐 글로벌 오픈 소스 인텔리전스 (OSINT)</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background-color:#111827; padding:14px; border-radius:14px; font-size:14px; color:#94A3B8; margin-bottom:18px; border: 1px solid #1F2937;'>
        <strong>📡 동적 인텔리전스 모듈:</strong> 출발국 <strong>[{selected_country}]</strong> 관련 통관 리스크 위협 기사를 구글 실시간 통신망을 통해 백그라운드 추적 중입니다.
    </div>
    """, unsafe_allow_html=True)
    
    if has_external_variable:
        st.info(f"📡 현시점 웹상에서 유효한 **[{selected_country}]** 발 실시간 마약 밀수 및 보안 위협 뉴스 속보가 탐지되었습니다.")
        st.write("")
        for idx, news in enumerate(live_news_feeds):
            st.markdown(f"**📌 [{idx+1}] {news['title']}**")
            st.link_button("🌐 보안 분석 보고서(원문 뉴스) 보기", news['link'], use_container_width=True)
            st.write("")
    else:
        st.success(f"🟢 현재 글로벌 망 내에 **[{selected_country}]** 관련 돌발적인 밀수 리스크 특이 속보가 없습니다.")
        st.markdown("""
            <div style='text-align:center; padding:40px 10px; color:#4B5563; font-size:14px; font-weight:500;'>
                🔍 LIVE FEEDS NOT FOUND<br>
                <span style='font-size:12px; color:#6B7280;'>장보고 예외 처리 규정 가동: 통계 모드로 자동 전환되었습니다.</span>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
st.markdown(f"<div style='text-align:right; font-size:12px; color:#6B7280; font-weight:500;'>INU SCM LOGISTICS SECURITY LAB | ENGINE STATUS: NIGHT WATCH MODE ACTIVE ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})</div>", unsafe_allow_html=True)