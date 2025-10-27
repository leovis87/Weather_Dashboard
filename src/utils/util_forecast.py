import pandas as pd
import streamlit as st

# 3. 가져온 날씨 데이터 가공
def process_forecast(data: dict) -> pd.DataFrame:
    """
    3시간 단위 데이터를 날짜별 최저/최고/평균 기온으로 요약
    """
    if data.get("cod") != "200" or "list" not in data:
        raise ValueError(f"예보 데이터가 유효하지 않습니다: {data.get('message', 'list 없음')}")

    df = pd.DataFrame(data["list"])

    # 날짜/시간 처리
        # dt_txt: "2025-10-26 12:00:00": str
        # pd.to_datetime: 날짜/시간 연산 가능
    df["dt_txt"] = pd.to_datetime(df["dt_txt"])
        # datetime에서 날짜(df["date"]부분만 추출)
    df["date"] = df["dt_txt"].dt.date

    # 기온 추출 (main은 dict)
        # main column: {"temp: 15.3, "humidity": 60, ...} -> dict
        # 그 중, temp 값만 뽑아서 temp column으로 생성
    df["temp"] = df["main"].apply(lambda x: x["temp"])

    # rain column이 dict일 때만 "3h" 값을 꺼냄. 없으면 0
    df["rain_3h"] = df["rain"].apply(lambda x: x.get('3h', 0) if isinstance(x, dict) else 0)

    # snow column이 dict일 때만 "3h" 값을 꺼냄. 없으면 0
    df["snow_3h"] = df["snow"].apply(lambda x: x.get('3h', 0) if isinstance(x, dict) else 0)

    # 습도
    df["humidity"] = df["main"].apply(lambda x: x["humidity"])

    # 풍속
    df["wind"] = df["wind"].apply(lambda x: x["speed"])


    # 날짜별 집계
        # date기준 groupby -> 하루 단위로 묶음
        # temp column에 대해 min, max, mean을 계산
    daily = (
        df.groupby("date")
          .agg(t_min=("temp", "min"),
               t_max=("temp", "max"),
               t_mean=("temp", "mean"),
               hu_min=("humidity", "min"),
               hu_max=("humidity", "max"),
               hu_mean=("humidity", "mean"),
               w_min=("wind", "min"),
               w_max=("wind", "max"),
               w_mean=("wind", "mean"),
               rain=("rain_3h", "sum"),
               mean_rain=("rain_3h", "mean"),
               max_rain=("rain_3h", "max"),
               snow=("snow_3h", "sum"),
               mean_snow=("snow_3h", "mean"),
               max_snow=("snow_3h", "max")
               )
    )

    # 사용자 친화적 column명으로 rename
    daily = daily.rename(columns = {
        "t_min": "최저기온",
        "t_max": "최대기온",
        "t_mean": "평균기온",
        "hu_min": "최저습도",
        "hu_max": "최대습도",
        "hu_mean": "평균습도",
        "w_min": "최저풍속",
        "w_max": "최대풍속",
        "w_mean": "평균풍속",
        "rain": "강수량",
        "mean_rain": "평균강수량",
        "max_rain": "최대강수량",
        "snow": "적설량",
        "mean_snow": "평균적설량",
        "max_snow": "최대적설량"
    })

    return daily

