#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@CODE:DATA-001 | SPEC: SPEC-DATA-001/spec.md

data.json 갱신 스크립트
국민연금 A값, 시장 수익률 등 외부 데이터를 갱신합니다.

사용법:
    python update_data.py

의존성:
    pip install requests (선택적 - API 호출 시 필요)
"""

import json
from datetime import datetime
from pathlib import Path

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent
DATA_FILE = PROJECT_ROOT / "data.json"


def get_nps_data() -> dict:
    """
    국민연금 관련 데이터 조회

    실제 운영 시에는 국민연금공단 API 또는 통계청 API를 사용할 수 있습니다.
    현재는 하드코딩된 값을 반환합니다 (2024년 기준).

    Returns:
        dict: 국민연금 데이터
    """
    return {
        "a_value": 2989352,           # 전년도 전체 가입자 평균소득 (원/년)
        "replacement_rate": 0.40,      # 소득대체율 (40%)
        "max_monthly_income": 5900000, # 기준소득월액 상한 (원/월)
        "min_monthly_income": 370000   # 기준소득월액 하한 (원/월)
    }


def get_market_data() -> dict:
    """
    시장 수익률 데이터 조회

    실제 운영 시에는 Yahoo Finance API 또는 한국거래소 API를 사용할 수 있습니다.
    현재는 하드코딩된 값을 반환합니다.

    Returns:
        dict: 시장 데이터
    """
    return {
        "sp500_10yr_avg": 0.10,   # S&P500 10년 평균 수익률 (10%)
        "kospi_10yr_avg": 0.05,   # KOSPI 10년 평균 수익률 (5%)
        "inflation_rate": 0.025   # 물가상승률 (2.5%)
    }


def get_wage_curve_data() -> dict:
    """
    연령별 임금상승률 데이터 조회

    실제 운영 시에는 고용노동부 또는 통계청 API를 사용할 수 있습니다.
    현재는 일반적인 한국 임금 곡선을 반영한 값을 반환합니다.

    Returns:
        dict: 임금상승률 데이터
    """
    return {
        "20s": 0.05,       # 20대: 연 5% 상승
        "30s": 0.05,       # 30대: 연 5% 상승
        "40s": 0.03,       # 40대: 연 3% 상승
        "50s_early": 0.00, # 50대 초반: 동결
        "50s_late": -0.02  # 55세 이후: 임금피크 2% 하락
    }


def update_data() -> dict:
    """
    data.json 파일 갱신

    Returns:
        dict: 갱신된 데이터
    """
    data = {
        "updated_at": datetime.now().strftime("%Y-%m-%d"),
        "nps": get_nps_data(),
        "market": get_market_data(),
        "wage_curve": get_wage_curve_data()
    }

    # JSON 파일 저장
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"data.json 갱신 완료: {DATA_FILE}")
    print(f"갱신일: {data['updated_at']}")

    return data


def validate_data() -> bool:
    """
    data.json 파일 유효성 검증

    Returns:
        bool: 유효성 여부
    """
    if not DATA_FILE.exists():
        print("ERROR: data.json 파일이 없습니다.")
        return False

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 필수 필드 검증
        required_fields = ["updated_at", "nps", "market", "wage_curve"]
        for field in required_fields:
            if field not in data:
                print(f"ERROR: 필수 필드 누락 - {field}")
                return False

        # 데이터 타입 검증
        if not isinstance(data["nps"]["a_value"], (int, float)):
            print("ERROR: nps.a_value는 숫자여야 합니다.")
            return False

        print("data.json 유효성 검증 통과")
        return True

    except json.JSONDecodeError as e:
        print(f"ERROR: JSON 파싱 오류 - {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("yourfuture 데이터 갱신 스크립트")
    print("=" * 50)

    # 데이터 갱신
    update_data()

    # 유효성 검증
    validate_data()

    print("=" * 50)
