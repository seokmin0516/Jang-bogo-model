import streamlit as st
import pandas as pd
import datetime

# 1. 페이지 레이아웃 최상단 설정
st.set_page_config(
    page_title="JARVIS : SCM Border Security Control Tower",
    page_icon="🤖",
    layout="wide"
)

# 2. 자비스 부팅 콘솔 텍스트 및 기본 헤더
st.code("SYSTEM STATUS: JARVIS BORDER SECURITY PROTOCOL ACTIVATED\nENCRYPTION LEVEL: MIL-SPEC AES-256", language="bash")
st.title("🤖 JARVIS : 국경 공급망 실시간 위험 통제탑")
st.caption("TACTICAL SCM RISK INTELLIGENCE & REAL-TIME MARITIME ANOMALY DETECTOR")
st.write("---")

# 3. 위험도 통계 마스터 데이터 매트릭스 (수학적 100점 만점 설계)
# [A] 국가 위험도 (순수 최고 4.7 배점 -> 국가 배점 만점은 50점)
country_risk_matrix = {
    '태국': 4.5, '미국': 4.2, '베트남': 3.8, '말레이시아': 3.5, 
    '중국(홍콩 포함)': 3.0, '라오스': 4.0, '독일': 2.8, '중남미(브라질 등)': 4.7
}

# [B] 품목별 위험밀도 (순수 최고 2.5 배점 -> 물품 배점 만점은 50점)
item_risk_matrix = {
    '커피 (HS 0901)': {'density': 2.5, 'lcl_weight': 1.5, 'desc': '강한 향으로 마약 탐지견의 후각 교란 유인 매우 높음'},
    '사탕, 초콜릿 (HS 1704)': {'density': 2.2, 'lcl_weight': 1.4, 'desc': '젤리나 사탕 모양으로 제조된 변종 마약(THC 등) 자체 위장 우범'},
    '화장품 (HS 3304)': {'density': 2.4, 'lcl_weight': 1.4, 'desc': '크림이나 액체 속에 녹이거나 이중 바닥 용기 내부 밀수 취약'},
    '시리얼, 곡물 (HS 1904)': {'density': 1.8, 'lcl_weight': 1.3, 'desc': '내용물 속 소량의 봉지 혼재 시 육안 식별 및 X-ray 판독 사각지대 존재'},
    '가방, 케이스 (HS 4202)': {'density': 2.0, 'lcl_weight': 1.3, 'desc': '가방 안감 및 캐리어 벽면 사이 라미네이트 이중 은닉 빈발'},
    '견과류, 과일 가공품 (HS 2008)': {'density': 1.5, 'lcl_weight': 1.2, 'desc': '밀폐 용기 내부 액체 혼재 및 실제 화물과의 밀도 유사성 악용'},
    '제재목 (HS 4407)': {'density': 0.5, 'lcl_weight': 1.1, 'desc': '원목 형태의 대형 화물, 대형 컨테이너 단위 밀수 유인'},
    '가죽 신발류 (HS 6403)': {'density': 1.6, 'lcl_weight': 1.3, 'desc': '두꺼운 신발 굽 및 밑창 공간 분해 후 고밀도 은닉 활용'},
    '자동자료처리기계 (HS 8471)': {'density': 0.8, 'lcl_weight': 1.1, 'desc': 'IT 장비 하우징 내부 디바이스 빈 공간 악용'},
    '기타 기계류 (HS 8479)': {'density': 0.7, 'lcl_weight': 1.1, 'desc': '대형 기계 구조물 내부 용접 밀봉형 은닉 수법 발생'},
    '가정용 전기기기 (HS 8509)': {'density': 1.4, 'lcl_weight': 1.2, 'desc': '가전 모터 및 배터리 팩 내부 공간 탈거 후 마약 적재 유입'}
}

# 4. 사이드바 프로파일링 인풋
st.sidebar.subheader("⚙️ OPERATIONAL INPUTS")
selected_country = st.sidebar.selectbox("1. 출발 국가(Origin) 선택", list(country_risk_matrix.keys()))
selected_item = st.sidebar.selectbox("2. 반입 품목(Item HS) 선택", list(item_risk_matrix.keys()))
cargo_type = st.sidebar.radio("3. 통관 유통 형태(SCM Variable)", ["LCL (소량 혼재 화물)", "FCL (단독 대량 화물)"])

# 5. 수학적으로 정밀한 100점 만점 환산 스코어링 알고리즘 코어
# [A] 국가 위험도 점수 산출 (최대값인 4.7점을 50점 만점으로 스케일링)
country_base = country_risk_matrix[selected_country]
final_country_risk = (country_base / 4.7) * 50.0

# [B] 물품 위험도 점수 산출 (LCL 가중치 적용 유무 분기 처리)
item_density = item_risk_matrix[selected_item]['density']
item_desc = item_risk_matrix[selected_item]['desc']

if cargo_type == "LCL (소량 혼재 화물)":
    scm_weight = item_risk_matrix[selected_item]['lcl_weight']
    status_alert = "🚨 [SYSTEM] LCL DIFFERENTIAL FILTER ENGAGED"
    # LCL일 때 나올 수 있는 물품 리스크 최대값은 커피 기준 2.5 * 1.5 = 3.75점
    # 이 최대값 3.75점을 물품 위험도 배점 한도인 50점 만점으로 정규화 환산
    raw_item_score = item_density * scm_weight
    final_item_risk = (raw_item_score / 3.75) * 50.0
else:
    scm_weight = 1.0
    status_alert = "✅ [SYSTEM] FCL STANDARD PROTOCOL APPLIED"
    # FCL일 때는 가중치가 배제되므로 순수 위험밀도 최대값인 2.5점을 50점 만점으로 환산
    final_item_risk = (item_density / 2.5) * 50.0

# [C] 최종 위험도 결합 (사용자 지정: 국가 위험도 + 최종 물품 위험도 = 100점 만점)
final_comprehensive_risk = final_country_risk + final_item_risk

# 6. 메인 화면 상단 - 계측 대시보드 컴포넌트 출력
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🌐 국가 위험도 (MAX 50.0)", 
        value=f"{final_country_risk:.1f} 점", 
        delta=f"출발지: {selected_country}"
    )

with col2:
    st.metric(
        label="📦 최종 물품 위험도 (MAX 50.0)", 
        value=f"{final_item_risk:.1f} 점", 
        delta=f"가중치 배율: x{scm_weight:.2f}"
    )

with col3:
    # 사용자 정의 커트라인 인디케이터 바인딩 (80점 이상 / 60점 이상 / 50점 이하)
    if final_comprehensive_risk >= 80.0:
        control_badge = "🚨 [즉시 개장검사 대상]"
    elif final_comprehensive_risk >= 60.0:
        control_badge = "⚠️ [유의 검사 대상]"
    elif final_comprehensive_risk <= 50.0:
        control_badge = "🟢 [안전 화물 통관]"
    else:
        control_badge = "🔵 [일반 모니터링 화물]"
        
    st.metric(
        label="🎯 종합 위험도 스케일 (MAX 100.0)", 
        value=f"{final_comprehensive_risk:.1f} 점", 
        delta=control_badge
    )

st.write("---")

# 7. 중간 화면 - 설명형 AI(XAI) 분석 엔진 & 실시간 인텔리전스 뉴스 2분할 대시보드
layout_col1, layout_col2 = st.columns([1.1, 0.9])

with layout_col1:
    st.subheader("🧠 자비스 리스크 진단 근거 (Explanation Dashboard)")
    
    # 정성적 가명 명세와 수식을 조합한 설명서 자동 생성
    st.info(f"""
    **[종합 모니터링 리포트]**
    * **국가 보안 프로파일링:** 분석 대상 화물은 누적 적발 규모가 높은 우범 권역인 **[{selected_country}]**을 통하여 국내 공급망에 진입하였습니다. 이에 의거하여 50점 만점 중 **{final_country_risk:.1f}점**의 국가 위험 가산 점수가 할당되었습니다.
    * **공급망 세그먼트 위험:** 본 화물은 통관 시 익명성과 소량 은닉 유인이 극대화되는 **[{cargo_type}]** 형태로 유입되었습니다. 이에 따라 시스템 알고리즘이 자동으로 해당 품목 고유의 차등 리스크 부하 배율인 **[x{scm_weight:.2f}]** 가중치 필터를 엔진에 주입하였습니다.
    * **품목 특성 분석:** 매칭된 **[{selected_item}]** 품목은 과거 범죄백서 분석 결과, *"{item_desc}"*라는 물리적 위장 취약점을 지니고 있습니다.
    * **결론 및 단속 제언:** 최종 산출 수식 `국가 환산점수({final_country_risk:.1f}) + 최종 물품 위험도({final_item_risk:.1f})`에 의해 총점 **{final_comprehensive_risk:.1f}점**이 도출되었습니다. 본 화물은 통제 규칙에 의거하여 현재 **{control_badge}** 등급 조치 처리가 필요합니다.
    """)
    
    # 정량 데이터 명세 매트릭스 표
    st.dataframe(
        pd.DataFrame({
            "위험 분석 지표 컴포넌트": ["출발지(Origin) 국가 환산 위험 점수", "품목별 기본 마약 위험밀도 점수", "SCM 물류 형태 가중치", "종합 보안 통제 스코어"],
            "정량 점수 스케일": [f"{final_country_risk:.1f} 점 / 50.0", f"{item_density:.1f} 점", f"x {scm_weight:.2f}", f"{final_comprehensive_risk:.1f} 점 / 100.0"]
        }),
        use_container_width=True
    )

with layout_col2: