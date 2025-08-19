from datetime import datetime, timedelta
from types import new_class

# # literal을 쓰지 않고 상수를 쓰는 이유
# 2라는 숫자가 "배송일이야" 라고 배경을 모르는 사람들
# (미래의 동료, 미래에 이 사실을 까먹은 나 자신)에게 알려주는 역할을 한다.
# magic number 를 쓰지 말자:
DELIVERY_DAYS = 2

def _is_holiday(day: datetime) -> bool:
    return day.weekday() > 5

def get_eta(purchase_date: datetime) -> datetime:
    current_date = purchase_date
    remaining_days = DELIVERY_DAYS

    while remaining_days > 0:
        current_date += timedelta(days=1)
        if not _is_holiday(current_date):
            remaining_days -= 1

    return current_date


def test_get_eta_2023_12_01() -> None:
    result = get_eta(datetime(2023, 12, 1))
    assert result == datetime(2023, 12, 4)


def test_get_eta_2024_12_31() -> None:
    """
    공휴일 정보가 없어서 1월 1일도 평일로 취급됩니다.
    """
    result = get_eta(datetime(2024, 12, 31))
    assert result == datetime(2025, 1, 2)


def test_get_eta_2024_02_28() -> None:
    result = get_eta(datetime(2024, 2, 28))
    assert result == datetime(2024, 3, 1)


def test_get_eta_2023_02_28() -> None:
    result = get_eta(datetime(2023, 2, 28))
    assert result == datetime(2023, 3, 2)
