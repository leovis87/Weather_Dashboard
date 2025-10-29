import streamlit as st
import pandas as pd
import uvicorn
import os
# from dotenv import load_dotenv # local 환경에서 실행 시 사용.
from api.openweather import get_forecast, \
                            get_current_weather_by_coords, \
                            get_location_by_ip
from utils.util_forecast import process_forecast
from ui.ui_forecast import show_forecast, \
                           show_current_details, \
                           show_current_weather
from fastapi import FastAPI

# # .env 파일에서 환경 변수를 로드
# load_dotenv()

# # os.getenv() 함수로 환경 변수 값을 가져옴
# API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

app = FastAPI()

API_KEY = st.secrets["OPENWEATHER_API_KEY"]

@app.get('/')
def main():
    return ""

def main():
    """
    각 기능별 함수들을 불러와
    UI를 표시
    """
    st.title("🌤️ 날씨 대시보드")

    # 1. 현재 위치(IP 기반) 자동 표시
    lat, lon, city_name = get_location_by_ip()
    if lat and lon:
        show_current_weather(lat, lon, f"📍 현재 위치: {city_name or '알 수 없음'}")
    
    st.divider()

    # 2. 내 위치 직접 입력
    st.subheader("📍 내 위치 직접 입력")
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        lat_input = st.number_input("위도",
                                    value=lat or 37.5665,
                                    format="%.6f")
    with c2:
        lon_input = st.number_input("경도",
                                    value=lon or 126.9780,
                                    format="%.6f")
    with c3:
        go = st.button("내 위치 날씨 보기")
    
    if go:
        current = get_current_weather_by_coords(lat_input, lon_input, API_KEY)

        if isinstance(current, dict) and str(current.get("cod")) == "200":
            show_current_details(current, "📍 사용자 지정 위치")
        else:
            st.error(
                f"사용자 지정 위치 호출 실패: "
                f"{current.get('message', '알 수 없는 오류') if isinstance(current, dict) else 'API 응답 오류'}"
            )
    
    st.divider()

    # 3. 도시 검색 -> 5일치 예보
    st.subheader("🔎 도시 검색(5일치 예보)")
    city = st.text_input("도시 이름을 입력하세요:", "서울")
    if st.button("날씨 조회"):
        data = get_forecast(city, API_KEY)

        if isinstance(data, dict) and str(data.get("cod")) == "200":
            try:            
                daily = process_forecast(data)
                show_forecast(daily)
            except Exception as e:
                st.error(f"데이터 가공 오류: {e}")
        else:
            st.error(
                f"도시를 찾을 수 없습니다: "
                f"{data.get('message', '알 수 없는 오류') if isinstance(data, dict) else 'API 응답 오류'}"
            )


if __name__ == "__main__":
    uvicorn.run("leovis:app",
                host="localhost",
                port=8000,
                reload=True)