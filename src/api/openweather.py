import requests

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

def get_weather(city_name: str,
                api_key: str) -> dict:
    """
    특정 도시의 현재 날씨 정보를 가져옴
    """

    # 한글 입력 -> 영어 변환
    query = CITY_MAP.get(city_name, city_name)
    # 만약 CITY_MAP에 없으면, 그대로 사용(예: 이미 영어로 입력한 경우)

    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": query,
        "appid": api_key,
        "units": "metric",  # 섭씨 단위
        "lang": "KR"        # 한국어 응답
    }
    response = requests.get(url, params=params)
    return response.json()


def get_forecast(city_name: str,
                 api_key: str) -> dict:
    """
    특정 도시의 5일치 3시간 단위 예보를 가져옴
    """

    # 한글 입력 -> 영어 변환
    query = CITY_MAP.get(city_name, city_name)
    # 만약 CITY_MAP에 없으면, 그대로 사용(예: 이미 영어로 입력한 경우)

    url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": query,
        "appid": api_key,
        "units": "metric",
        "lang": "KR"
    }
    response = requests.get(url, params=params)
    return response.json()