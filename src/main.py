import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from api.openweather import get_weather, get_forecast


# .env 파일에서 환경 변수를 로드
load_dotenv()

# os.getenv() 함수로 환경 변수 값을 가져옴
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

def main():
    """
    Streamlit 기반 날씨 대시보드 메인 함수.

    주요 동작
    ----------------------
    1. 사용자 입력으로 도시 이름 받음.
    2. OpenWeatherMap API를 호출, 날씨 데이터를 가져옴.
    3. 현재 날씨와 주요 정보를 화면에 표시.

    Parameters
    ----------------------
    없음 (Streamlit 위젯을 통해 입력 받음)

    Returns
    ----------------------
    웹 브라우저에 날씨 정보 UI를 렌더링
    """
    st.title("🌤️ Weather Dashboard")
    city = st.text_input("도시 이름을 입력하세요:", "서울")

    if st.button("날씨 조회"):
        api_key = API_KEY
        weather = get_weather(city, api_key)
        forecast = get_forecast(city, api_key)

        if weather.get("cod") != 200:
            st.error(f"error발생: {forecast.get('message')}. 도시를 찾을 수 없습니다.")
        else:
            # 24시간 예보 데이터 정리

            times, temps, rains = [], [], []
            for item in forecast["list"][:8]:   # 3시간 x 8 = 24시간
                times.append(item["dt_txt"])
                temps.append(item["main"]["temp"])
                rains.append(item.get("rain", {}).get("3h", 0))

            # DataFrame으로 변환

            df = pd.DataFrame({
                "시간": times,
                "기온(°C)": temps,
                "강수량(mm)": rains
            })

            st.subheader(f"{city}의 24시간 예보 데이터")
            st.dataframe(df)

            # 라인 차트 (시간 vs 기온/강수량)
            st.subheader("📈 라인 차트")
            st.line_chart(df.set_index("시간")[["기온(°C)", "강수량(mm)"]])

            # 막대 차트 (시간 vs 강수량)
            st.subheader("📊 막대 차트 (강수량)")
            st.bar_chart(df.set_index("시간")["강수량(mm)"])

            # st.metric("온도 (°C)", weather['main']['temp'])
            # st.metric("습도 (%)", weather['main']['humidity'])
            # st.write(f"☁️ {weather['weather'][0]['description']}")

            # st.subheader("24시간 예보")
            # rain_expected = False
            # for item in forecast["list"][:8]:
            #     time = item["dt_txt"]
            #     desc = item["weather"][0]["description"]

            #     # 강수량 확인 (없으면 0mm)
            #     rain = item.get("rain", {}).get("3h", 0)

            #     st.write(f"{time} → {desc}, 🌧️ 강수량: {rain} mm")

            #     if rain > 0:
            #         rain_expected = True

            # if rain_expected:
            #     st.warning("☔ 앞으로 24시간 안에 비가 올 예정입니다!")
            # else:
                # st.success("🌞 앞으로 24시간은 비 예보가 없습니다.")

if __name__ == "__main__":
    main()