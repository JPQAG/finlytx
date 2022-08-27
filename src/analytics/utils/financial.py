from typing import Dict, List
import datetime

from analytics.utils.cashflow import match_cashflow_to_discount_curve

from .date_time import years_between_dates


def present_value_of_cashflows(
    pricing_date: datetime.date, 
    cashflows: List[Dict],
    discount_curve: List[Dict]
) -> float:
    present_value_result = 0.0

    cashflows_and_discount_curve = match_cashflow_to_discount_curve(cashflows, discount_curve)

    for cashflow_and_discount in cashflows_and_discount_curve:
        result = present_value(
            pricing_date,
            cashflow_and_discount["date"],
            cashflow_and_discount["cashflow_value"],
            cashflow_and_discount["discount_rate"],
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


def discount_rate(
    pricing_date: datetime.date,
    cashflow_date: datetime.date,
    present_value: float,
    future_value: float
) -> None:
    number_of_years = years_between_dates(pricing_date, cashflow_date)

    result = ((future_value/present_value)**(1/number_of_years)) -1

    return result
