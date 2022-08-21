from typing import Dict, List
import datetime

from .date_time import years_between_dates


def present_value_of_cashflows(
    pricing_date: datetime.date, cashflows: List[Dict]
) -> float:
    present_value_result = 0.0

    for cashflow in cashflows:
        result = present_value(
            pricing_date,
            cashflow["date"],
            cashflow["cashflow_value"],
            cashflow["discount_rate"],
        )

        present_value_result += result

    return present_value_result


def present_value(
    pricing_date: datetime.date,
    cashflow_date: datetime.date,
    future_value: float,
    discount_rate: float,
) -> float:
    number_of_years = years_between_dates(pricing_date, cashflow_date)

    return (future_value) / ((1 + discount_rate) ** (number_of_years))


def future_value(
    pricing_date: datetime.date,
    cashflow_date: datetime.date,
    present_value: float,
    discount_rate: float,
) -> float:
    number_of_years = years_between_dates(pricing_date, cashflow_date)

    result = present_value * ((1 + discount_rate) ** number_of_years)

    return result


def discount_rate() -> None:
    pass
