import streamlit as st
import pandas as pd
import datetime

# 1. 페이지 레이아웃 및 국경 수호신 '장보고' 제어탑 설정
st.set_page_config(
    page_title="JANG BOGO : SCM Border Security Control Tower",
    page_icon="⚓",
    layout="wide"
)

# 2. 장보고 시스템 부팅 콘솔 텍스트 및 헤더 (완전 블랙 감성)
st.code("SYSTEM STATUS: JANG BOGO MARITIME SECURITY PROTOCOL ACTIVATED\nANTI-INFLATION ENGINE: STABLE | THEME: JET BLACK COMPLIANT", language="bash")
st.title("⚓ 장보고(JANG BOGO) : 국경 공급망 실시간 위험 통제탑")
st.caption("INTELLIGENT SCM RISK PREDICTION ENGINE & REAL-TIME MARITIME ANOMALY DETECTOR")
st.write("---")

# 3. 위험도 통계 마스터 데이터 매트릭스 (수학적 100점 만점 설계)
country_risk_matrix = {
    '태국': 4.5, '미국': 4.2, '베트남': 3.8, '말레이시아': 3.5, 
    '중국(홍콩 포함)': 3.0, '라오스': 4.0, '독일': 2.8, '중남미(브라질 등)': 4.7
}

item_risk_matrix = {
    '커피 (HS 0901)': {'density': 2.5, 'lcl_weight': 1.5, 'desc': '강한 향으로 마약 탐지견의 후각을 교란하기 위해 가장 흔히 사용됨'},
    '사탕, 초콜릿 (HS 1704)': {'density': 2.2, 'lcl_weight': 1.4, 'desc': '젤리나 사탕 모양으로 제조된 변종 마약(THC 젤리 등) 자체 위장 우범'},
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

# 5. [장보고 엔진] 차등 가중치 100점 만점 조절 알고리즘
# [A] 국가 위험도 억제 (만점을 30점으로 제한하여 인플레이션 방지)
country_base = country_risk_matrix[selected_country]
final_country_risk = (country_base / 4.7) * 30.0

# [B] 물품 위험도 강화 (만점을 70점으로 상향하여 LCL 변수 영향력 극대화)
item_density = item_risk_matrix[selected_item]['density']
item_desc = item_risk_matrix[selected_item]['desc']

if cargo_type == "LCL (소량 혼재 화물)":
    scm_weight = item_risk_matrix[selected_item]['lcl_weight']
    status_alert = "🚨 [ENGINE] LCL DIFFERENTIAL FILTER ENGAGED"
    raw_item_score = item_density * scm_weight
    final_item_risk = (raw_item_score / 3.75) * 70.0
else:
    scm_weight = 1.0
    status_alert = "✅ [ENGINE] FCL STANDARD PROTOCOL APPLIED"
    final_item_risk = (item_density / 2.5) * 40.0  # FCL 안전 디카운트 혜택 반영

# [C] 최종 위험도 결합 (국가 30점 + 물품 70점 = 100점 만점)
final_comprehensive_risk = final_country_risk + final_item_risk

# 6. 메인 화면 상단 - 계측 대시보드 컴포넌트 출력
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🌐 국가 보정 지수 (MAX 30.0)", 
        value=f"{final_country_risk:.1f} 점", 
        delta=f"출발지: {selected_country}"
    )

with col2:
    st.metric(
        label="📦 최종 SCM 물품 지수 (MAX 70.0)", 
        value=f"{final_item_risk:.1f} 점", 
        delta=f"물류 배율: x{scm_weight:.2f}"
    )

with col3:
    # 요청하신 엄격한 컷오프 규칙 매칭
    if final_comprehensive_risk >= 80.0:
        control_badge = "🚨 [즉시 개장검사 대상]"
    elif final_comprehensive_risk >= 60.0:
        control_badge = "⚠️ [유의 검사 대상]"
    elif final_comprehensive_risk <= 50.0:
        control_badge = "🟢 [안전 화물 통관]"
    else:
        control_badge = "🔵 [일반 모니터링 화물]"
        
    st.metric(
        label="🎯 종합 통제 위험도 (MAX 100.0)", 
        value=f"{final_comprehensive_risk:.1f} 점", 
        delta=control_badge
    )

st.write("---")

# 7. 중간 화면 - 설명형 AI(XAI) 분석 엔진 & 실시간 인텔리전스 뉴스 2분할 대시보드
layout_col1, layout_col2 = st.columns([1.1, 0.9])

with layout_col1:
    st.subheader("🧠 장보고 리스크 진단 근거 (Explanation Dashboard)")
    
    st.info(f"""
    **[점수 변별력 최적화 리포트]**
    * **국가 가중치 최적화:** 무조건적인 점수 고공행진을 막기 위해 국가 리스크의 총 배점을 **30점**으로 제한했습니다. **[{selected_country}]**발 화물은 국가 리스크 점수 **{final_country_risk:.1f}점**이 반영되었습니다.
    * **공급망 세그먼트 위험 변별력:** 밀수의 핵심 경로인 **[{cargo_type}]**의 단속 효과를 극대화하기 위해 물품 지수 배점을 **70점**으로 대폭 상향 조정했습니다. LCL 유통 경로의 사각지대를 적발하기 위해 **[x{scm_weight:.2f}]** 배율이 정상 작동 중입니다.
    * **품목 특성 분석:** 매칭된 **[{selected_item}]** 품목은 *"{item_desc}"*라는 물리적 위장 우범성이 존재합니다.
    * **결론 및 단속 제언:** `국가 보정점수({final_country_risk:.1f}) + 최종 SCM 물품점수({final_item_risk:.1f})` 수식에 의해 최종 총점 **{final_comprehensive_risk:.1f}점**이 도출되었습니다. 한정된 관세 인력의 효율적 배치를 위해 본 화물은 현재 **{control_badge}** 조치 처리를 제안합니다.
    """)
    
    st.dataframe(
        pd.DataFrame({
            "위험 분석 지표 컴포넌트": ["출발지(Origin) 국가 환산 점수 (30점 만점)", "품목별 SCM 물품 위험 점수 (70점 만점)", "SCM 물류 형태 가중치 배율", "종합 보안 통제 스코어 (100점 만점)"],
            "정량 점수 스케일": [f"{final_country_risk:.1f} 점 / 30.0", f"{final_item_risk:.1f} 점 / 70.0", f"x {scm_weight:.2f}", f"{final_comprehensive_risk:.1f} 점 / 100.0"]
        }),
        use_container_width=True
    )

with layout_col2:
    st.subheader("📡 실시간 국경 인텔리전스 통신망 피드")
    
    news_tab1, news_tab2 = st.tabs(["💊 GLOBAL DRUG INTELLIGENCE", "🚢 MARITIME & SCM ISSUE"])
    
    with news_tab1:
        st.caption("🚨 `LIVE FEED: 글로벌 마약 우범 적발 속보 및 검증 출처`")
        
        st.error("**[방금 전]** 미국 DEA, 동남아발 LCL 컨테이너 내부 화장품 제형 은닉 필로폰 45kg 단속")
        st.link_button("🔗 DEA(미 마약단속국) 공식 보도자료 확인", "https://www.dea.gov")
        st.write("")
        
        st.warning("**[10분 전]** 태국 람차방 항만, 화물 가방 내벽 안감에 라미네이트 수법으로 숨긴 코카인 밀수 조직 적발")
        st.link_button("🔗 관세청(KCS) 마약 적발 사례집 조회", "https://www.customs.go.kr")
        st.write("")
        
        st.info("**[1시간 전]** UNODC 보고서 발표: 골든 트라이앵글 유입 필로폰 국내 소매가 전년 대비 14% 변동 폭 확대")
        st.link_button("🔗 UNODC World Drug Report 데이터셋", "https://www.unodc.org")
            
    with news_tab2:
        st.caption("🔵 `LIVE FEED: 글로벌 해운물류 리드타임 이상징후 및 검증 출처`")
        
        st.info("**[실시간]** 싱가포르 항만 CFS 혼재 창고 화물 체류 시간(Dwell Time) 표준 대비 36시간 돌발 정체 발생")
        st.link_button("🔗 MPA(싱가포르 항만청) 실시간 정체 지수", "https://www.mpa.gov.sg")
        st.write("")
        
        st.warning("**[30분 전]** 파나마 운하 통항 제한 여파로 소형 포워더 우회 항로(LCL 환적) 탐색 징후 증가")
        st.link_button("🔗 파나마 운하청(ACP) 선박 통항 그리드", "https://pancanal.com")
        st.write("")
        
        st.code("LOG: CONGESTION INDEX HIGH AT EAST ASIA ROUTE", language="bash")

st.write("---")
st.text(f"SYSTEM LOG: JANG BOGO SCORING ENGINE ACTIVATED AT {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | VERSION 4.0-BLACK")