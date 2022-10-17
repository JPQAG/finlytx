from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Dict, List
from src.analytics.utils.cashflow import get_most_recent_cashflow

from src.analytics.utils.date_time import days_between_dates, months_between_dates, years_between_dates

def calculate_macaulay_duration(
    pricing_date: datetime,
    dirty_price: float,
    cashflows: List[Dict],
    yield_to_final: float 
) -> float:
    """Calculate the Macaulay duration of a set of cashflows.

    *CFA22LVL12021Book5Pg15*

    https://www.nber.org/system/files/chapters/c6342/c6342.pdf  

    \dfrac{\sum_{i=1}^{n}
    \dfrac{(i-\dfrac{t}{T})*PMT}{(1+r)^{i-\dfrac{t}{T}}}}
    {PV}

    t= Number of days from the last coupon payment to the settlement date.
    T= Number of days in the coupon period.
    t/T= Fraction of the coupon period that has gone by since the last payment.
    PMT= Coupon payment per period.
    FV= Future value paid at maturity, or the par value of the bond.
    PV= Present Value of future cashflows (discount at yield). Therefore current dirty price.
    r= Yield to maturity, or th market discount rate, per period.
    N= The number of evenly spaced periods to maturity as of the beginning of the current period. 

    Args:
        pricing_date (datetime.datetime)
        dirty_price (float): Present value of cashflows discounted at yield_to_final.
        cashflows (List[Dict]): Array of cashflow object (date, cashflow_value)
        yield_to_final (float): Yield to final cashflow in decimal form.

    Returns:
        float: The Macaulay Duration of the cashflows.
    """
    days_between_coupon_dates = days_between_dates(cashflows[0]["date"], cashflows[1]["date"])
    periods_per_year = round(365 / days_between_coupon_dates)
    start_of_first_period_date = cashflows[0]["date"] - timedelta(days=days_between_coupon_dates)
    previous_cashflow_date = get_most_recent_cashflow(pricing_date, cashflows)["date"] if pricing_date >= cashflows[0]["date"] else start_of_first_period_date
    number_of_periods_remaining = years_between_dates(start_of_first_period_date, cashflows[-1]["date"]) * periods_per_year

    t = days_between_dates(previous_cashflow_date, pricing_date)
    T = days_between_coupon_dates
    t_T = t/T
    FV = cashflows[-1]["cashflow_value"]
    r = yield_to_final
    N = None

    numerator = 0
    denominator = dirty_price
    for i in range(0, int(round(number_of_periods_remaining)) + 1):
        PMT = cashflows[i]["cashflow_value"]

        # TODO: Change so that N is based on cashflow date.
        N = i if i == (number_of_periods_remaining) else (i + 1)
        
        numerator += (((N-t_T)*PMT)/((1+r)**(N-t_T)))
       
    macaulay_duration = numerator / denominator

    return macaulay_duration
