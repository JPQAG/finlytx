import datetime

from typing import Dict, List

from analytics.utils.financial import discount_rate_of_cashflows
from analytics.utils.cashflow import trim_cashflows_after_workout

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

def z_spread() -> None:
    pass

def g_spread() -> None:
    pass

def oas_spread() -> None:
    pass

def i_spread() -> None:
    pass

def spread_to_benchmark(
    pricing_date: datetime.datetime,
    cashflows: List[Dict],
    present_value: float,
    workout_date: datetime.datetime,
    benchmark_curve: List[Dict]
) -> float:
    """Calculate the annualised spread to benchmark to a defined workout date using present 
        value of cashflows and the benchmark curve.

        #TODO: Interpolate curves and regression. 

    Args:
        pricing_date (datetime.datetime): Date to which cashflows are discounted.
        cashflows (List[Dict]): Cashflows between pricing and final cashflow.
        present_value (float): Present value (usually price/pricing value).
        workout_date (datetime.datetime): Redemption date (call/maturity etc).
        benchmark_curve (List[Dict]): Dates and rates of benchmark curve.

    Returns:
        float: Annualised spread to benchmark rate.
    """