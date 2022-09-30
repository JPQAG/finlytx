import datetime
from dateutil.relativedelta import relativedelta
from typing import Dict, List

from src.analytics.utils.date_time import years_between_dates




def generate_cashflows() -> None:
    pass

def match_cashflow_to_discount_curve(
    cashflows: List[Dict],
    discount_curve: List[Dict]
) -> List[Dict]:
    """Match cashflows to discount rates by date.

    Args:
        cashflows (List[Dict]): Cashflow series
        discount_curve (List[Dict]): Discount curve series.

    Returns:
        List[Dict]: Combined date, cashflow value and discount rate.
    """

    matched_list = []

    for cashflow in cashflows:
        for rate in discount_curve:
            if rate['date'] == cashflow["date"]:
                matched_list.append(
                    {
                        "date": cashflow["date"],
                        "cashflow_value": cashflow["cashflow_value"],
                        "discount_rate": rate["discount_rate"]
                    }
                )

    return matched_list

def sum_cashflows(
    cashflows: List[Dict]
) -> float:
    """Calulate the sum of a series of cashflows.

    Args:
        cashflows (List[Dict]): Cashflow series (date, cashflow_value)

    Returns:
        float: Sum of cashflows.
    """

    sum = 0

    for cashflow in cashflows:
        sum += cashflow['cashflow_value']
    
    return sum

def trim_cashflows_after_workout(
    cashflows: List[Dict],
    workout_date: datetime.datetime
) -> List[Dict]:
    """Trim the cashflows to exclude any cashflows after workout date.


    Args:
        cashflows (List[Dict]): Date and value of cashflows.
        workout_date (datetime.datetime): Date after which cashflows will be excluded.

    Returns:
        List[Dict]: The included cashflows.
    """

    included_cashflows = []

    for cashflow in cashflows:
        if cashflow["date"] <= workout_date:
            included_cashflows.append(cashflow)

    return included_cashflows

def generate_fixed_cashflows(
    starting_date: datetime.datetime,
    ending_date: datetime.datetime,
    periods_per_year: float,
    face_value: float,
    coupon_rate: float,
    arrears: bool=True,
    redemption_discount: float=0
) -> List[Dict]:
    """_summary_

    Args:
        starting_date (datetime.datetime): Starting date of the first period.
        ending_date (datetime.datetime): Ending date of the final period/
        periods_per_year (float): Number of periods per year.
        face_value (float): The face value of the security.
        coupon_rate (float): Coupon rate of the security.
        arrears (bool, optional): Payments in arrears or advance. Defaults to True.

    Returns:
        List[Dict]: List of objects containing cashflows(date, cashflow value)
    """
    cashflows_array = []

    first_payment_date = starting_date + relativedelta(years=(1/periods_per_year)) if arrears else starting_date
    number_of_periods = years_between_dates(starting_date, ending_date)*periods_per_year

    for i in range(0, number_of_periods):
        cashflow_date = first_payment_date + relativedelta(years=(i/periods_per_year))
        cashflow_value = coupon_rate * face_value
        cashflows_array.append(
            {
                "date": cashflow_date,
                "cashflow_value": cashflow_value
            }
        )
        if (i == number_of_periods - 1):
            cashflows_array.append(
                {
                    "date": cashflow_date,
                    "cashflow_value": face_value * (1 - redemption_discount)
                }
            )

    return cashflows_array