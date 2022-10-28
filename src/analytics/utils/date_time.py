import datetime
from typing import Any, List
import pandas as pd

from src.analytics.utils.lookup import TIMESERIES_TIME_PERIODS

def days_between_dates(first_date: datetime.datetime, second_date: datetime.datetime) -> float:
    """Time between two dates in days.

    Args:
        first_date (datetime.datetime): The earlier date.
        second_date (datetime.datetime): The later date.

    Returns:
        float: The decimal value representing the number of whole days between two dates.
    """
    return (second_date - first_date).days

def months_between_dates(first_date: datetime.datetime, second_date: datetime.datetime) -> float:
    """Time between two dates in months and fractions of months.

    Args:
        first_date (datetime.datetime): The earlier date.
        second_date (datetime.datetime): The later date.

    Returns:
        float: The decimal value representing the number of whole and part months between the dates.
    """
    return ( second_date.year - first_date.year) * 12 + second_date.month - first_date.month

def years_between_dates(first_date: datetime.datetime, second_date: datetime.datetime, days_in_year: int=365) -> float:
    """Time between two dates in years and fractions of years.

    Args:
        first_date (datetime.datetime): The earlier date.
        second_date (datetime.datetime): The later date.

    Returns:
        float: The decimal value representing the number of whole and part years between the dates.
    """
    return days_between_dates(first_date, second_date)/days_in_year

def generate_date_range(
    start_date: datetime.datetime, 
    end_date: datetime.datetime, 
    freq_input: TIMESERIES_TIME_PERIODS.keys,
    arrears: bool = True
    ) -> List:
    """_summary_

    Args:
        start_date (datetime.datetime): _description_
        end_date (datetime.datetime): _description_
        freqInput (str): _description_
        arrears (bool): _description_

    Returns:
        List: _description_
    """
    assert freq_input in TIMESERIES_TIME_PERIODS.keys, f"'{freq_input}' is not in {TIMESERIES_TIME_PERIODS.keys}"
    assert start_date <= end_date, f"'{start_date}' is after {end_date}"
    
    if freq_input == "A":
        date_range = _annual_range(start_date, end_date, freq_input)
    else: 
        date_range = _monthly_range(start_date, end_date, freq_input)

    return date_range.pop() if arrears else date_range[:-1]

def _annual_range(
    start_date,
    end_date,
    freq
) -> List:
    return pd.date_range(start_date, end_date, freq=pd.offset(years=1))

def _monthly_range(
    start_date,
    end_date,
    freq
) -> List:
    assert freq in TIMESERIES_TIME_PERIODS.keys, f"'{freq}' is not in {TIMESERIES_TIME_PERIODS.keys}"
    assert start_date <= end_date, f"'{start_date}' is after {end_date}"

    rng = pd.date_range(pd.Timestamp(start_date)-pd.offsets.MonthBegin(),
                        end_date,
                        freq='MS')
    ret = (rng + pd.offsets.Day(pd.Timestamp(start_date).day-1)).to_series()
    ret.loc[ret.dt.month > rng.month] -= pd.offsets.MonthEnd(1)
    return pd.DatetimeIndex(ret)