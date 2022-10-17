import datetime
from typing import List
from dateutil.relativedelta import relativedelta
import pandas as pd

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
    freq: str,
    arrears: bool
    ) -> List:
    
    date_range = pd.date_range(start_date, periods=periods, freq=pd.DateOffset(years=1))


    return [d.strftime("%Y-%m-%d") for d in date_range]

def _get_start_date(
    start_date: datetime.datetime,
    arrears: bool
    )