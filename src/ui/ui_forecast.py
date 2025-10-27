import pandas as pd
import streamlit as st

def show_forecast(daily: pd.DataFrame):
    """
    Streamlit에서 예보 테이블과 그래프를 출력
    """
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
    st.line_chart(daily[["최저기온", "최대기온", "평균기온"]])

def show_current_details(data: dict,
                         title: str):
    """
    현재 날씨 상세(강수량/습도/풍속 등) 출력
    """
    st.subheader(title)
    main = data.det("main", {})
    wind = data.det("wind", {})
    rain = data.det("rain", {})
    snow = data.det("snow", {})

    cols = st.columns(4)
    cols[0].metric("기온(°C)", f"{main.get('temp', '—')}")
    cols[1].metric("체감온도(°C)", f"{main.get('feels_like', '—')}")
    cols[2].metric("습도(%)", f"{main.get('humidity', '—')}")
    cols[3].metric("바람(m/s)", f"{wind.get('speed', '—')}")

    # 선택적 강수/적설 표시
    if "1h" in rain:
        st.write(f"☔ 최근 1시간 강수량: {rain['1h']} mm")
    if "1h" in snow:
        st.write(f"❄️ 최근 1시간 적설량: {snow['1h']} mm")
