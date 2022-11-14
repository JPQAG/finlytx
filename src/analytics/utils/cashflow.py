import datetime
from dateutil.relativedelta import relativedelta
from typing import Dict, List

from src.analytics.utils.date_time import generate_date_range, years_between_dates
from src.analytics.utils.lookup import TIMESERIES_TIME_PERIODS


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

def generate_cashflows(
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    cashflow_freq: float,
    face_value: float,
    coupon_rate: float,
    arrears: bool=True,
    variable_coupon: bool=False,
    underlying_curve: List=[],
    redemption_discount: float=0.00
) -> List[Dict]:
    """Generates cashflows from a start_date to end_date. 

    *The end_date specifies the final cashflow date. Thus the start of subsequent periods is the day after the cashflow date (in arrears).

    Args:
        starting_date (datetime.datetime): Starting date of the first period.
        ending_date (datetime.datetime): Ending date of the final period/
        periods_per_year (float): Number of periods per year.
        face_value (float): The face value of the security.
        coupon_rate (float): Annual coupon rate of the security.
        arrears (bool, optional): Payments in arrears or advance. Defaults to True.
        variable_coupon (bool, optional): Coupons are variable. Default to False.
        underlying_curve (List): Underlying benchmark curve to get forward rate forecast.

    Returns:
        List[Dict]: List of objects containing cashflows(date, cashflow value)
    """
    assert all(isinstance(date, (datetime.datetime)) for date in [start_date, end_date]), f"Date arguments must be of type datetime."
    assert cashflow_freq in TIMESERIES_TIME_PERIODS.keys(), f"'{cashflow_freq}' is not in {TIMESERIES_TIME_PERIODS.keys()}."
    assert all(isinstance(float_val, float) for float_val in [face_value, coupon_rate, redemption_discount]), f"Numeric args must be of float type."
    # TODO: FLOATING RATE

    date_range = generate_date_range(start_date, end_date, freq_input=cashflow_freq)
    annual_frequency = TIMESERIES_TIME_PERIODS[cashflow_freq]['annual_frequency']
    cashflows_array = []

    for date in date_range:
        coupon_rate_periodic = "_get_variable_cashflow(date, underlying_curve)" if variable_coupon else (coupon_rate/annual_frequency)
        if date == date_range[-1]:
            cashflow = ( face_value * coupon_rate_periodic ) + face_value
        else:
            cashflow = ( face_value * coupon_rate_periodic )
        cashflows_array.append(
            {
                'date': date,
                'cashflow': cashflow
            }
        )

    return cashflows_array

def get_most_recent_cashflow(
    reference_date: datetime.datetime,
    cashflows: List[Dict]
) -> Dict:
    """Find the closest last occuring cashflow object relative to a reference date.

    Args:
        reference_date (datetime.datetime): The date to which 'last occurring' is relative.
        cashflows (List[Dict]): A security's cashflows in which we are finding the most recent.

    Returns:
        Dict: The cashflow dictionary for the most recent cashflow.
    """
    if not cashflows: 
        raise ValueError("Cashflows array empty.")
    elif reference_date < cashflows[0]["date"]:
        raise ValueError("Reference date before first cashflow date.")

    most_recent_cashflow = cashflows[0]

    for cashflow in cashflows:
        most_recent_cashflow = cashflow if cashflow["date"] <= reference_date else most_recent_cashflow
    
    return most_recent_cashflow
