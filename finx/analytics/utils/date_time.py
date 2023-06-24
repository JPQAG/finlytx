import datetime

import pandas as pd
from typing import List
from pandas.tseries.offsets import DateOffset

from finx.analytics.utils.lookup import TIMESERIES_TIME_PERIODS

def get_days_before_date(
    start_date: datetime.datetime,
    number_of_days: int,
    is_calendar_days: bool=True
) -> datetime.datetime:
    return (start_date - datetime.timedelta(days=number_of_days))

def get_record_date(
    payment_date: datetime.datetime,
    ex_record_config: dict
) -> datetime.datetime:
    
    num_days = ex_record_config['record_date']['days_before_payment_date']
    
    return get_days_before_date(payment_date, num_days)

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
    freq_input: TIMESERIES_TIME_PERIODS.keys()="A",
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
    assert isinstance(start_date, datetime.datetime), f"start_date must be of type datetime.datetime"
    assert isinstance(end_date, datetime.datetime), f"end_date must be of type datetime.datetime"
    assert start_date <= end_date, f"start_date is after end_date"
    assert freq_input in TIMESERIES_TIME_PERIODS.keys(), f"'{freq_input}' is not in {TIMESERIES_TIME_PERIODS.keys()}"

    if freq_input == "A":
        date_range = _annual_range(start_date, end_date)
    else: 
        date_range = _n_monthly_range(start_date, end_date, freq_input)

    range_as_list = date_range.to_native_types().tolist()

    return_list = range_as_list[1:] if arrears else range_as_list[:-1]

    return  return_list

def _annual_range(
    start_date: datetime.datetime,
    end_date: datetime.datetime
) -> List:
    assert isinstance(start_date, datetime.datetime), f"start_date must be of type datetime.datetime"
    assert isinstance(end_date, datetime.datetime), f"end_date must be of type datetime.datetime"
    assert start_date <= end_date, f"start_date is after end_date"

    return pd.date_range(start_date, end_date, freq=DateOffset(years=1))

def _n_monthly_range(
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    freq: TIMESERIES_TIME_PERIODS.keys()
) -> List:
    assert freq in TIMESERIES_TIME_PERIODS.keys(), f"'{freq}' is not in {TIMESERIES_TIME_PERIODS.keys}"
    assert start_date <= end_date, f"'{start_date}' is after {end_date}"

    monthly_range = _monthly_range(start_date, end_date)
    n_monthly_range = _get_n_monthly(monthly_range, freq)

    return n_monthly_range

def _monthly_range(
    start_date: datetime.datetime,
    end_date: datetime.datetime,
) -> pd.DatetimeIndex:
    assert isinstance(start_date, datetime.datetime), f"start_date must be of type datetime.datetime"
    assert isinstance(end_date, datetime.datetime), f"end_date must be of type datetime.datetime"
    assert start_date <= end_date, f"start_date is after end_date"
    
    day_of_month = start_date.day
    is_start_of_month = day_of_month == 1

    date_range_month_start = _generate_pd_date_range(
        (start_date - pd.offsets.MonthBegin()) if not is_start_of_month else start_date,
        end_date,
        freq='MS'
    )

    return_index = date_range_month_start if day_of_month == 1 else _mid_month_adj(start_date, date_range_month_start)

    return return_index

def _generate_pd_date_range(
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    freq: str,
    inclusive: str="both"
) -> pd.DatetimeIndex:
    return_index = pd.date_range(
        start_date,
        end_date,
        freq=freq,
        inclusive=inclusive
    )

    return return_index

def _mid_month_adj(
    start_date: datetime.datetime,
    date_range: pd.DatetimeIndex
) -> pd.DatetimeIndex:
    assert isinstance(date_range, pd.DatetimeIndex), f"'{date_range}' is not of type pd.DatetimeIndex."
    assert isinstance(start_date, datetime.datetime), f"'{start_date}' is not of type datetime.datetime."
    
    day_offset: int = pd.Timestamp(start_date).day - 1
    offset: pd.offsets.Day = pd.offsets.Day(day_offset)
    date_range_day_adjusted: pd.Series = (date_range + offset).to_series()
    date_range_day_adjusted.loc[date_range_day_adjusted.dt.month > date_range.month] -= pd.offsets.MonthEnd(1)

    return pd.DatetimeIndex(date_range_day_adjusted)

def _get_n_monthly(
    date_list: List[datetime.datetime],
    freq: TIMESERIES_TIME_PERIODS.keys()
) -> List[datetime.datetime]:
    assert len(date_list) != 0, f"'{date_list}' is empty."
    assert all(isinstance(date, (datetime.datetime)) for date in date_list), f"{date_list} elements must be of type datetime.datetime."
    assert freq in TIMESERIES_TIME_PERIODS.keys(), f"{freq} is not in {TIMESERIES_TIME_PERIODS.keys()}"

    date_interval = int(12/TIMESERIES_TIME_PERIODS[freq]["annual_frequency"])

    filtered_list = date_list[0::date_interval]

    return filtered_list

def _default_date(
    date: str
) -> datetime.datetime:
    assert isinstance(date, str), f"'{date}' is not of type string."

    return datetime.datetime.strptime(date, "%Y-%m-%d")
