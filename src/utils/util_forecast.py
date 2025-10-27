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

    # 날짜별 집계
        # date기준 groupby -> 하루 단위로 묶음
        # temp column에 대해 min, max, mean을 계산
    daily = (
        df.groupby("date")["temp"]
          .agg(min="min", max="max", mean="mean")
    )

    # 사용자 친화적 column명으로 rename
    daily = daily.rename(columns = {
        "min": "최저기온",
        "max": "최대기온",
        "mean": "평균기온"
    })

    return daily