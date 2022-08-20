from datetime import date
from sqlite3 import Date
from typing import Dict, List
import datetime

from .date_time import years_between_dates


def series_present_value(
    pricing_date: datetime.date,
    cashflows: List[Dict]
) -> float:
    present_value = 0
    
    for cashflow in cashflows:
        
        present_value += 1
        
def discount_future_value(
    pricing_date: datetime.date,
    cashflow_date: datetime.date,
    future_value: float,
    discount_rate: float    
) -> float:
    number_of_years = years_between_dates(pricing_date, cashflow_date)
    
    return (future_value)/(1+discount_rate)^(number_of_years)
    
def future_value():
    pass

def discount_rate():
    pass
