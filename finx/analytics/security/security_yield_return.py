import datetime

from typing import Dict, List

from finx.analytics.utils.financial import discount_rate_of_cashflows
from finx.analytics.utils.cashflow import trim_cashflows_after_workout
from finx.analytics.utils.curve import construct_ns_curve, construct_nss_curve
from finx.analytics.utils.helper import calculate_years_between_dates

def yield_to_workout(
    pricing_date: datetime.datetime,
    cashflows: List[Dict],
    present_value: float,
    workout_date: datetime.datetime
) -> float:
    """Calculate the annualised yield to a defined workout date using present 
        value of cashflows.

    Args:
        pricing_date (datetime.datetime): Date to which cashflows are discounted.
        cashflows (List[Dict]): Cashflows between pricing and final cashflow.
        present_value (float): Present value (usually price/pricing value).
        workout_date (datetime.datetime): Redemption date (call/maturity etc)

    Returns:
        float: Annualised yield.
    """

    workout_cashflows = trim_cashflows_after_workout(
        cashflows,
        workout_date
    )
    
    yield_to_workout = discount_rate_of_cashflows(
        pricing_date,
        workout_cashflows,
        present_value
    )

    return yield_to_workout

def current_yield(
    face_value: float,
    coupon_rate: float,
    market_price: float
) -> float:
    """Calculate the current/running yield of a security at a defined
        market price.

    Args:
        face_value (float): The security's face value.
        coupon_rate (float): The security's actual/forecast coupon.
        market_price (float): Price for which current yield is calculated.

    Returns:
        float: The current yield.
    """
    coupon = coupon_rate * face_value

    current_yield = coupon / market_price

    return current_yield

def z_spread():
    pass

def g_spread(
    pricing_date: datetime.datetime,
    cashflows: List[Dict],
    present_value: float,
    workout_date: datetime.datetime,
    government_curve: List[Dict],
    interpolation_method: str=['ns', 'nss']
) -> float:
    """The difference between the yield and government rate at a specified 
        workout date.

    Args:
        pricing_date (datetime.datetime): Date to which cashflows are discounted.
        cashflows (List[Dict]): Cashflows between pricing and final cashflow.
        present_value (float): Present value (usually price/pricing value).
        workout_date (datetime.datetime): Redemption date (call/maturity etc).
        government_curve (List[Dict]): Dates and rates of benchmark curve.
        interpolation_method (str): Method used to interpolate benchmark_curve.

    Returns:
        float: Annualised spread to government curve.
    """

    g_spread = spread_to_benchmark(
        pricing_date,
        cashflows,
        present_value,
        workout_date,
        government_curve,
        interpolation_method
    )

    return g_spread

def i_spread(
    pricing_date: datetime.datetime,
    cashflows: List[Dict],
    present_value: float,
    workout_date: datetime.datetime,
    swap_curve: List[Dict],
    interpolation_method: str=['ns', 'nss']
) -> float:
    """The difference between the yield and swap rate at a specified 
        workout date.

    Args:
        pricing_date (datetime.datetime): Date to which cashflows are discounted.
        cashflows (List[Dict]): Cashflows between pricing and final cashflow.
        present_value (float): Present value (usually price/pricing value).
        workout_date (datetime.datetime): Redemption date (call/maturity etc).
        swap_curve (List[Dict]): Dates and rates of benchmark curve.
        interpolation_method (str): Method used to interpolate benchmark_curve.

    Returns:
        float: Annualised spread to swap curve.
    """

    i_spread = spread_to_benchmark(
        pricing_date,
        cashflows,
        present_value,
        workout_date,
        swap_curve,
        interpolation_method
    )

    return i_spread

def spread_to_benchmark(
    pricing_date: datetime.datetime,
    cashflows: List[Dict],
    present_value: float,
    workout_date: datetime.datetime,
    benchmark_curve: List[Dict],
    interpolation_method: str=['ns', 'nss']
) -> float:
    """Calculate the annualised spread to benchmark to a defined workout date using present 
        value of cashflows and the benchmark curve.

    Args:
        pricing_date (datetime.datetime): Date to which cashflows are discounted.
        cashflows (List[Dict]): Cashflows between pricing and final cashflow.
        present_value (float): Present value (usually price/pricing value).
        workout_date (datetime.datetime): Redemption date (call/maturity etc).
        benchmark_curve (List[Dict]): Dates and rates of benchmark curve.
        interpolation_method (str): Method used to interpolate benchmark_curve.

    Returns:
        float: Annualised spread to benchmark rate.
    """

    curve = None
    if interpolation_method == 'ns':
        curve = construct_ns_curve(pricing_date, benchmark_curve)
    elif interpolation_method == 'nss':
        curve = construct_nss_curve(pricing_date, benchmark_curve)

    target_tenor = calculate_years_between_dates(pricing_date, workout_date)
    benchmark_rate_at_tenor = curve(target_tenor)

    yield_to_workout_date = yield_to_workout(
        pricing_date,
        cashflows,
        present_value,
        workout_date
    )

    spread = yield_to_workout_date - benchmark_rate_at_tenor

    return spread