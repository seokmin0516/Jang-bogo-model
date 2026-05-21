import streamlit as st
import pandas as pd
import numpy as np

# 1. 페이지 기본 설정 및 하이엔드 테마 스타일링
st.set_page_config(
    page_title="관세 국경 SCM 실시간 위험도 모니터링 컨트롤 타워",
    page_icon="🚢",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    h1 { color: #1B365D; font-family: 'Malgun Gothic', sans-serif; font-weight: bold; }
    h3 { color: #2C3E50; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #1B365D; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
""", unsafe_html=True)

st.title("🚢 국경 SCM 실시간 우범 공급망 모니터링 시스템")
st.subheader("물류 형태(LCL/FCL) 및 국가·품목 복합 리스크 매트릭스 엔진")

# 2. 내부 마스터 하드코딩 데이터 세팅 (전처리 및 누락 방지 안정화)
# [A] 국가별 기본 위험도 마스터 (최근 분기별 적발 빈도 및 규모 가중치)
country_risk_matrix = {
    '태국': 4.5, '미국': 4.2, '베트남': 3.8, '말레이시아': 3.5, 
    '중국(홍콩 포함)': 3.0, '라오스': 4.0, '독일': 2.8, '중남미(브라질 등)': 4.7
}

# [B] 품목별 순수 위험밀도 및 고유 가중치 테이블
item_risk_matrix = {
    '커피 (HS 0901)': {'density': 2.5, 'lcl_weight': 1.5, 'desc': '강한 향으로 탐지견 후각 교란 유인 높음'},
    '사탕, 초콜릿 (HS 1704)': {'density': 2.2, 'lcl_weight': 1.4, 'desc': '변종 마약(THC 젤리 등) 자체 위장 우범'},
    '화장품 (HS 3304)': {'density': 2.4, 'lcl_weight': 1.4, 'desc': '액체/크림 유통 및 이중 용기 제작 취약'},
    '시리얼, 곡물 (HS 1904)': {'density': 1.8, 'lcl_weight': 1.3, 'desc': '육안 및 X-ray 판독 사각지대 활용'},
    '가방, 케이스 (HS 4202)': {'density': 2.0, 'lcl_weight': 1.3, 'desc': '내부 벽면 라미네이트 이중 은닉 다수'},
    '견과류, 과일 가공품 (HS 2008)': {'density': 1.5, 'lcl_weight': 1.2, 'desc': '캔/병 내부 내용물 혼재 우범'},
    '제재목 (HS 4407)': {'density': 0.5, 'lcl_weight': 1.1, 'desc': '원목 형태, 대형 화물 위주'},
    '가죽 신발류 (HS 6403)': {'density': 1.6, 'lcl_weight': 1.3, 'desc': '신발 굽 및 내부 빈 공간 활용'},
    '자동자료처리기계 (HS 8471)': {'density': 0.8, 'lcl_weight': 1.1, 'desc': 'B2B 기계 장비 내부 공간 악용'},
    '기타 기계류 (HS 8479)': {'density': 0.7, 'lcl_weight': 1.1, 'desc': 'B2B 기계 구조물 은닉 수법'},
    '가정용 전기기기 (HS 8509)': {'density': 1.4, 'lcl_weight': 1.2, 'desc': '소형 가전 내부 부품 분해 후 은닉'}
}

# 3. 사용자 인터페이스(UI) 사이드바 구성
st.sidebar.header("📥 실시간 화물 프로파일링 입력")

selected_country = st.sidebar.selectbox("1. 출발 국가(지역) 선택", list(country_risk_matrix.keys()))
selected_item = st.sidebar.selectbox("2. 반입 품목 코드 선택", list(item_risk_matrix.keys()))
cargo_type = st.sidebar.radio("3. 화물 반입 형태(SCM Variable)", ["LCL (소량 혼재 화물)", "FCL (단독 대량 화물)"])

# 4. 실시간 동적 리스크 연산 코어 알고리즘
country_base_risk = country_risk_matrix[selected_country]
item_density = item_risk_matrix[selected_item]['density']
item_desc = item_risk_matrix[selected_item]['desc']

# 사용자의 로직 반영: LCL일 때만 가중치 활성화, FCL이면 가중치 1.0(배제)
if cargo_type == "LCL (소량 혼재 화물)":
    scm_weight = item_risk_matrix[selected_item]['lcl_weight']
    status_text = "⚠️ LCL 공급망 사각지대 가중치 필터 작동 중"
else:
    scm_weight = 1.0
    status_text = "✅ FCL 단독 컨테이너 안전 표준 가중치 적용 (가중치 배제)"

# 종합 위험도 산출 공식
scm_adjusted_item_risk = item_density * scm_weight
final_comprehensive_risk = country_base_risk * scm_adjusted_item_risk

# 5. 메인 대시보드 화면 렌더링 및 대칭 시각화
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="🌐 국가별 기본 위험 지수", value=f"{country_base_risk:.2f} / 5.00", delta=selected_country)

with col2:
    st.metric(label="📦 SCM 보정 품목 위험밀도", value=f"{scm_adjusted_item_risk:.2f}", delta=f"적용 가중치: x{scm_weight:.2f}", delta_color="inverse" if scm_weight > 1.0 else "normal")

with col3:
    # 최종 점수 기반 위험 등급 분류
    if final_comprehensive_risk >= 6.0:
        badge = "🚨 [심각] 즉시 정밀 개장 검사 대상"
    elif final_comprehensive_risk >= 3.5:
        badge = "⚠️ [주의] X-ray 집중 판독 대상"
    else:
        badge = "🟢 [일반] 상시 선별 검사 대상"
    st.metric(label="🎯 최종 컴플라이언스 종합 위험도", value=f"{final_comprehensive_risk:.2f}", delta=badge, delta_color="off")

st.markdown("---")

# 6. 실무 데이터 매칭 컨텍스트 서술 파트
st.subheader("🔍 프로파일링 대상 화물 SCM 명세 분석")
detail_df = pd.DataFrame({
    "평가 변수 항목": ["분석 대상 국가", "타겟 품목명", "은닉 특성 리스크 리포트", "선택된 공급망 형태", "최종 리스크 매트릭스 수식"],
    "상세 모니터링 데이터": [
        selected_country,
        selected_item,
        item_desc,
        cargo_type,
        f"국가 지수({country_base_risk}) × [품목 밀도({item_density}) × 가중치({scm_weight})] = {final_comprehensive_risk:.2f}"
    ]
})
st.table(detail_df)

st.info(f"💡 **시스템 메시지:** {status_text} | 현업 단속용 실시간 API 연결 대기 중.")