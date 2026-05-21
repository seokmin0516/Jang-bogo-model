import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정 (가장 최상단에 위치)
st.set_page_config(
    page_title="관세 국경 SCM 실시간 위험도 모니터링",
    page_icon="🚢",
    layout="wide"
)

# 2. 타이틀 및 헤더 표시 (충돌 우려가 있는 마크다운 스타일 수정을 안전한 표준 방식으로 우회)
st.title("🚢 국경 SCM 실시간 우범 공급망 모니터링 시스템")
st.caption("물류 형태(LCL/FCL) 및 국가·품목 복합 리스크 매트릭스 엔진")
st.write("---")

# 3. 내부 위험도 평가 마스터 데이터 정의
country_risk_matrix = {
    '태국': 4.5, '미국': 4.2, '베트남': 3.8, '말레이시아': 3.5, 
    '중국(홍콩 포함)': 3.0, '라오스': 4.0, '독일': 2.8, '중남미(브라질 등)': 4.7
}

item_risk_matrix = {
    '커피 (HS 0901)': {'density': 2.5, 'lcl_weight': 1.5, 'desc': '강한 향으로 탐지견 후각 교란 유인 높음'},
    '사탕, 초콜릿 (HS 1704)': {'density': 2.2, 'lcl_weight': 1.4, 'desc': '변종 마약(THC 젤리 등) 자체 위장 우범'},
    '화장품 (HS 3304)': {'density': 2.4, 'lcl_weight': 1.4, 'desc': '액체/크림 유통 및 이중 용기 제작 취약'},
    '시리얼, 곡물 (HS 1904)': {'density': 1.8, 'lcl_weight': 1.3, 'desc': '내용물 속 소량 혼재 시 육안 식별 불가'},
    '가방, 케이스 (HS 4202)': {'density': 2.0, 'lcl_weight': 1.3, 'desc': '가방 안감 사이 라미네이트 이중 은닉'},
    '견과류, 과일 가공품 (HS 2008)': {'density': 1.5, 'lcl_weight': 1.2, 'desc': '캔/병 내부 내용물과 밀도 유사성 악용'},
    '제재목 (HS 4407)': {'density': 0.5, 'lcl_weight': 1.1, 'desc': '원목 형태의 대형 B2B 화물'},
    '가죽 신발류 (HS 6403)': {'density': 1.6, 'lcl_weight': 1.3, 'desc': '신발 굽 및 밑창 내부 빈 공간 활용'},
    '자동자료처리기계 (HS 8471)': {'density': 0.8, 'lcl_weight': 1.1, 'desc': 'IT 장비 내부 디바이스 공간 악용'},
    '기타 기계류 (HS 8479)': {'density': 0.7, 'lcl_weight': 1.1, 'desc': '대형 기계 구조물 정밀 내부 은닉'},
    '가정용 전기기기 (HS 8509)': {'density': 1.4, 'lcl_weight': 1.2, 'desc': '가전 부품 분해 후 내부 공간 밀수'}
}

# 4. 사이드바 인터페이스 구성
st.sidebar.header("📥 실시간 화물 프로파일링 입력")

selected_country = st.sidebar.selectbox("1. 출발 국가(지역) 선택", list(country_risk_matrix.keys()))
selected_item = st.sidebar.selectbox("2. 반입 품목 코드 선택", list(item_risk_matrix.keys()))
cargo_type = st.sidebar.radio("3. 화물 반입 형태(SCM Variable)", ["LCL (소량 혼재 화물)", "FCL (단독 대량 화물)"])

# 5. 핵심 리스크 연산 로직 (LCL일 때만 가중치 반영, FCL이면 가중치 배제)
country_base_risk = country_risk_matrix[selected_country]
item_density = item_risk_matrix[selected_item]['density']
item_desc = item_risk_matrix[selected_item]['desc']

if cargo_type == "LCL (소량 혼재 화물)":
    scm_weight = item_risk_matrix[selected_item]['lcl_weight']
    status_alert = "⚠️ LCL 공급망 사각지대 차등 가중치 필터 실시간 작동 중"
else:
    scm_weight = 1.0
    status_alert = "✅ FCL 단독 컨테이너 안전 표준 적용 (우범 가중치 배제)"

# 최종 리스크 지수 계산
scm_adjusted_item_risk = item_density * scm_weight
final_comprehensive_risk = country_base_risk * scm_adjusted_item_risk

# 6. 리스크 계측 대시보드 렌더링
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🌐 국가 리스크")
    st.info(f"**{selected_country} 기본 지수**\n\n {country_base_risk:.2f} / 5.00")

with col2:
    st.subheader("📦 SCM 물류 리스크")
    st.warning(f"**보정 위험밀도: {scm_adjusted_item_risk:.2f}**\n\n적용 배율: x{scm_weight:.2f}")

with col3:
    st.subheader("🎯 종합 통제 등급")
    if final_comprehensive_risk >= 6.0:
        st.error(f"**점수: {final_comprehensive_risk:.2f}**\n\n🚨 [심각] 즉시 개장 검사")
    elif final_comprehensive_risk >= 3.5:
        st.warning(f"**점수: {final_comprehensive_risk:.2f}**\n\n⚠️ [주의] X-ray 집중 판독")
    else:
        st.success(f"**점수: {final_comprehensive_risk:.2f}**\n\n🟢 [일반] 상시 선별 검사")

st.write("---")

# 7. 상세 명세 테이블 서술
st.subheader("🔍 프로파일링 대상 화물 SCM 상세 분석 리포트")

report_data = {
    "평가 변수 항목": ["분석 대상 국가", "타겟 품목명", "은닉 특성 리스크", "선택된 공급망 형태", "최종 리스크 연산식"],
    "상세 모니터링 데이터": [
        selected_country,
        selected_item,
        item_desc,
        cargo_type,
        f"국가 지수({country_base_risk}) × [품목 밀도({item_density}) × 가중치({scm_weight})] = {final_comprehensive_risk:.2f}"
    ]
}

df_report = pd.DataFrame(report_data)
st.table(df_report)

st.write(f"💡 **시스템 메시지:** {status_alert}")