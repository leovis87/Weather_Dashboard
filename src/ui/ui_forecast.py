import pandas as pd
import streamlit as st
from api.openweather import get_current_weather_by_coords
from utils.util_forecast import check_rain_alert, check_snow_alert

API_KEY = st.secrets["OPENWEATHER_API_KEY"]

def show_forecast(daily: pd.DataFrame):
    """
    Streamlit에서 예보 테이블과 그래프를 출력
    """
    st.info(check_rain_alert(daily), check_snow_alert(daily))

    # 제목/설명 텍스트 출력
    st.write("📊 5일치 예보 요약")
    # DataFrame을 표 형태로 보여줌
        # use_container_width=False:
        #   표의 가로 크기가 데이터프레임 자체 크기에 맞춤
        # use_container_width=True:
        #   표가 Streamlit 앱의 전체 가로 폭을 차지하도록 확장
    st.dataframe(daily, use_container_width=True)

    # date를 index로 설정 -> x축 날짜
    # 최저기온, 최고기온, 평균기온 -> y축
    tab1, tab2, tab3, tab4 = st.tabs(["🌡️ 기온", "💧 습도", "🌬️ 풍속", "☔ 강수/적설"])
    with tab1:
        st.line_chart(daily[["최저기온","최대기온","평균기온"]])
    with tab2:
        st.line_chart(daily[["최저습도","최대습도","평균습도"]])
    with tab3:
        st.line_chart(daily[["최저풍속","최대풍속","평균풍속"]])
    with tab4:
        st.line_chart(daily[["강수량","최대강수량","적설량","최대적설량"]])


def show_current_weather(lat: float,
                         lon: float,
                         title: str):
    """
    현재 위치 날씨를 안전하게 가져와서 출력
    """
    current = get_current_weather_by_coords(lat,
                                            lon,
                                            API_KEY)
    
    # 1. 응답이 dict인지 확인
    if not isinstance(current, dict):
        st.error("API 응답이 올바르지 않습니다.")
        return

    # 2. 정상 응답 여부 확인
    cod = str(current.get("cod", "500"))
    if cod != "200":
        st.error(f"{title} 호출 실패: {current.get('message', '알 수 없는 오류')}")
        return
    
    # 3. 정상일 때만 상세 출력
    show_current_details(current, title)

def show_current_details(data: dict,
                         title: str):
    """
    현재 날씨 상세(강수량/습도/풍속 등) 출력
    """
    st.subheader(title)
    main = data.get("main", {})
    wind = data.get("wind", {})
    rain = data.get("rain", {})
    snow = data.get("snow", {})

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌡️ 온도", f"{main.get('temp', 'N/A')} °C")
    with col2:
        st.metric("💧 습도", f"{main.get('humidity', 'N/A')} %")
    with col3:
        st.metric("🌬️ 풍속", f"{wind.get('speed', 'N/A')} m/s")

    # 강수량 표시
    if rain:
        st.info(f"☔ 최근 1시간 강수량: {rain.get('1h', 0)} mm / 최근 3시간: {rain.get('3h', 0)} mm")
    if snow:
        st.info(f"❄️ 최근 1시간 적설량: {snow.get('1h', 0)} mm / 최근 3시간: {snow.get('3h', 0)} mm")

