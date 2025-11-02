import requests
import pandas as pd
import streamlit as st

API_KEY = st.secrets["OPENWEATHERMAP_API_KEY"]

"""
특정 도시의 현재 날씨 정보를 OpenWeatherMap API에서 가져옴.

Parameters
----------------------
city_name: str
조회할 도시 이름 (예: "Seoul)

api_key: str
OpenWeatherMap에서 발급받은 개인 API 키.

Returns
----------------------
dict
날씨 정보가 담긴 JSON 응답을 파이썬 dict 형태로 반환.
예: {"weather": [...], "main": {...}, "wind": {...}}
"""

CITY_MAP = {
    "서울": "Seoul",
    "부산": "Busan",
    "대구": "Daegu",
    "인천": "Incheon",
    "광주": "Gwangju",
    "대전": "Daejeon",
    "울산": "Ulsan"
}

# 1. 특정 장소의 데이터 가져오기 => API 호출
def get_weather(city_name: str,
                API_KEY: str) -> dict:
    """
    특정 도시의 현재 날씨 정보를 가져옴 => API 호출
    """

    # 한글 입력 -> 영어 변환
    query = CITY_MAP.get(city_name, city_name)
    # 만약 CITY_MAP에 없으면, 그대로 사용(예: 이미 영어로 입력한 경우)

    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": query,
        "appid": API_KEY,
        "units": "metric",  # 섭씨 단위
        "lang": "KR"        # 한국어 응답
    }
    response = requests.get(url, params=params, timeout=10)
    return response.json()


# 2. 날씨 데이터 가져오기 => API 호출
def get_forecast(city_name: str,
                 API_KEY: str) -> dict:
    """
    특정 도시의 5일치 3시간 단위 예보를 가져옴 => API 호출
    """

    # 한글 입력 -> 영어 변환
    query = CITY_MAP.get(city_name, city_name)
    # 만약 CITY_MAP에 없으면, 그대로 사용(예: 이미 영어로 입력한 경우)

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={query}&appid={API_KEY}&units=metric&lang=kr"
    params = {
        "q": query,
        "appid": API_KEY,
        "units": "metric",
        "lang": "KR"
    }
    response = requests.get(url, params=params, timeout=10)
    return response.json()

# 3. 위도(lat), 경도(lon)로 현재 날씨를 가져옴
def get_current_weather_by_coords(lat: float,
                                  lon: float,
                                  API_KEY: str) -> dict:
    """
    위도(latitude): lat
    경도(longitude): lon
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=kr"
    try:
        response = requests.get(url, timeout = 10)
        return response.json()  # 실패해도 dict 반환
    except Exception as e:
        return {"cod": "500", "message": str(e)}

# 4. IP 기반 대략적인 위치를 가져옴 => API 사용
def get_location_by_ip() -> tuple[float | None,
                                  float | None,
                                  str | None]:
    """
    tuple로 항목을 가져옴
    """
    try:
        data = requests.get("https://ip-api.com/json/", timeout=8).json()
        return data.get("lat"), data.get("lon"), data.get("city")
    except Exception:
        return None, None, None
