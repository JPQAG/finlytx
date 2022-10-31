import datetime
from os import stat
from typing import Any, List
import pandas as pd
from pandas.tseries.offsets import DateOffset

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
    freq_input: TIMESERIES_TIME_PERIODS.keys(),
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
    assert freq_input in TIMESERIES_TIME_PERIODS.keys(), f"'{freq_input}' is not in {TIMESERIES_TIME_PERIODS.keys()}"
    assert start_date <= end_date, f"'{start_date}' is after {end_date}"
    
    if freq_input == "A":
        date_range = _annual_range(start_date, end_date, freq_input)
    else: 
        date_range = _monthly_range(start_date, end_date, freq_input)

    return_list = date_range.to_native_types().tolist()[1:] if arrears else date_range[:-1].to_native_types().tolist()

    return  return_list

def _annual_range(
    start_date,
    end_date,
    freq
) -> List:
    return pd.date_range(start_date, end_date, freq=DateOffset(years=1))

def _monthly_range(
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    freq: TIMESERIES_TIME_PERIODS.keys()
) -> List:
    assert freq in TIMESERIES_TIME_PERIODS.keys(), f"'{freq}' is not in {TIMESERIES_TIME_PERIODS.keys}"
    assert start_date <= end_date, f"'{start_date}' is after {end_date}"
    
    day_of_month = datetime.datetime.strptime(start_date, "%Y-%m-%d").day
    annual_freq = TIMESERIES_TIME_PERIODS[freq]["annual_frequency"]
    monthly_interval = int(12 / annual_freq)

    date_range_start_of_month = pd.date_range(
        pd.Timestamp(start_date)-pd.offsets.MonthBegin(),
        end_date,
        freq='MS'
    )

    return_index = date_range_start_of_month if day_of_month == 1 else _mid_month_adj(start_date, date_range_start_of_month)

    filtered = return_index.to_series().iloc[::monthly_interval]

    return pd.DatetimeIndex(filtered)

def _mid_month_adj(
    start_date: datetime.datetime,
    date_range: pd.DatetimeIndex
) -> pd.DatetimeIndex:
    day_offset: int = pd.Timestamp(start_date).day - 1
    offset: pd.offsets.Day = pd.offsets.Day(day_offset)
    date_range_day_adjusted: pd.Series = (date_range + offset).to_series()
    date_range_day_adjusted.loc[date_range_day_adjusted.dt.month > date_range.month] -= pd.offsets.MonthEnd(1)
    return pd.DatetimeIndex(date_range_day_adjusted)