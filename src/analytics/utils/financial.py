from typing import Dict, List
import datetime

from analytics.utils.cashflow import match_cashflow_to_discount_curve
from analytics.utils.cashflow import sum_cashflows

from .date_time import years_between_dates


def present_value_of_cashflows(
    pricing_date: datetime.date, 
    cashflows: List[Dict],
    discount_curve: List[Dict]
) -> float:
    """Calculate the present value of future cashflows that are discounted
        at distinct discount (interest) rates.

    Args:
        pricing_date (datetime.date): Date to which cashflows are discounted.
        cashflows (List[Dict]): Cashflows between pricing and final cashflow.
        discount_curve (List[Dict]): Curve of discount rates.

    Returns:
        float: present value.
    """
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
    """Calculate the present value of a cashflow compounded annually at a defined
        discount (interest) rate.

    Args:
        pricing_date (datetime.date): Date to which cashflows are discounted.
        cashflow_date (datetime.date): Date of cashflow.
        future_value (float): Future value of cashflow.
        discount_rate (float): Interest rate used to discount.

    Returns:
        float: _description_
    """
    number_of_years = years_between_dates(pricing_date, cashflow_date)

    return (future_value) / ((1 + discount_rate) ** (number_of_years))

def future_value(
    pricing_date: datetime.date,
    cashflow_date: datetime.date,
    present_value: float,
    discount_rate: float,
) -> float:
    """Calculate the future value of a cashflow compounded annually at a defined
        discount (interest) rate.

    Args:
        pricing_date (datetime.date): Date to which cashflows are discounted.
        cashflow_date (datetime.date): Date of the future cashflow.
        present_value (float): Value at pricing_date.
        discount_rate (float): Interest rate.

    Returns:
        float: _description_
    """
    number_of_years = years_between_dates(pricing_date, cashflow_date)

    result = present_value * ((1 + discount_rate) ** number_of_years)

    return result

def discount_rate_of_cashflows(
    pricing_date: datetime.timedelta,
    cashflows: List[Dict],
    present_value: float
) -> float:
    """Calculate interest rate (discount rate) that discounts sum of cashflows
        (future value) to present value.

    Args:
        pricing_date (datetime.delta): Date to which cashflows are discounted.
        cashflows (List[Dict]): Cashflows between pricing and final cashflow.
        present_value (float): Present value (usually price/pricing value).
        future_value (float): Sum of cashflow values.

    Returns:
        float: discount rate.
    """

    future_value = sum_cashflows(cashflows)

    final_cashflow_date = cashflows[-1]['date']

    discount_interest_rate = discount_rate(
        pricing_date, 
        final_cashflow_date,
        present_value,
        future_value
    )

    return discount_interest_rate

def discount_rate(
    pricing_date: datetime.date,
    cashflow_date: datetime.date,
    present_value: float,
    future_value: float
) -> float:
    """Calculate interest rate (discount rate) that discounts a cashflow
        (future value) to present value.

    Args:
        pricing_date (datetime.date): Date to which cashflows are discounted.
        cashflow_date (datetime.date): Cashflows between pricing and final cashflow.
        present_value (float): Present value (usually price/pricing value).
        future_value (float): Sum of cashflow values.

    Returns:
        float: discount rate.
    """
    number_of_years = years_between_dates(pricing_date, cashflow_date)

    result = ((future_value/present_value)**(1/number_of_years)) -1

    return result
