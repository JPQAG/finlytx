from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Dict, List
from src.analytics.utils.cashflow import get_most_recent_cashflow
from src.analytics.utils.date_time import (
    _default_date
)

from src.analytics.utils.date_time import (days_between_dates, months_between_dates, years_between_dates)
from src.analytics.utils.financial import (present_value)

def INCOMPLETE_calculate_macaulay_duration(
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
    days_between_coupon_dates = days_between_dates(
        _default_date(cashflows[0]["date"]['payment_date']), 
        _default_date(cashflows[1]["date"]['payment_date']),
    )
    periods_per_year = round(365 / days_between_coupon_dates)
    start_of_first_period_date = _default_date(cashflows[0]["date"]['payment_date']) - timedelta(days=days_between_coupon_dates)
    most_recent_cashflow = get_most_recent_cashflow(pricing_date, cashflows)["date"]
    previous_cashflow_date = most_recent_cashflow if pricing_date >= _default_date(cashflows[0]["date"]['payment_date']) else start_of_first_period_date
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

def calculate_macaulay_duration(
    pricing_date: datetime,
    dirty_price: float,
    cashflows: List[Dict],
    yield_to_final: float
) -> float:
    simple_cashflows = [
        {'date': _default_date(cashflow['date']['payment_date']), 'cashflow': cashflow['cashflow']['total']}
        for cashflow
        in cashflows
    ]
    settlement_before_first_cashflow = days_between_dates(simple_cashflows[0]['date'], pricing_date) < 1
    
    if settlement_before_first_cashflow:
        days_in_coupon_period = days_between_dates(simple_cashflows[0]['date'], simple_cashflows[1]['date'])
        most_recent_cashflow = simple_cashflows[0]['date'] - timedelta(days=days_in_coupon_period)
        days_into_current_coupon_period = days_between_dates(pricing_date, most_recent_cashflow)
    else:
        most_recent_cashflow = get_most_recent_cashflow(pricing_date, simple_cashflows)
        days_into_current_coupon_period = days_between_dates(most_recent_cashflow['date'], pricing_date)
        
    coupon_period_in_days = days_between_dates(
        simple_cashflows[0]['date'],
        simple_cashflows[1]['date']
    )
    
    relevant_cashflows = [
        cashflow for cashflow 
        in cashflows 
        if _default_date(cashflow['date']['payment_date']) > pricing_date
    ]
    
    periods = range(1, len(relevant_cashflows))
    times_to_receipt = [
        ((ind + 1) - days_into_current_coupon_period/coupon_period_in_days)
        for ind, payment_date
        in enumerate(relevant_cashflows)
    ]
    cashflows = [cashflow['cashflow']['total'] for cashflow in relevant_cashflows]
    present_values = [
        present_value(pricing_date, _default_date(cashflow['date']['payment_date']), cashflow['cashflow']['total'], yield_to_final)
        for cashflow
        in relevant_cashflows
    ]
    total_present_value = sum(present_values)
    weights = [
        present_value / total_present_value
        for present_value
        in present_values
    ]
    
    time_x_weight = [
        time * weight
        for time, weight
        in zip(times_to_receipt, weights)
    ]
    
    macaulay_duration = sum(time_x_weight)
    
    return macaulay_duration

def calculate_modified_duration(
    macaulay_duration: float,
    yield_per_period: float,
    periods_per_year: float = 1
) -> float:
    return (macaulay_duration / (1 + yield_per_period)) / periods_per_year
