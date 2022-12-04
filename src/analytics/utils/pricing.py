import datetime
from typing import Any, Dict, List

from src.analytics.utils.date_time import(
    days_between_dates,
    _default_date
)

def get_accrued_interest(
    pricing_date: datetime.datetime,
    period_start: datetime.datetime,
    period_end: datetime.datetime,
    record_date: datetime.datetime,
    coupon_payment_amount: float
) -> float:
    assert (period_start <= pricing_date <= period_end), "pricing_date must be >= period_start and <= period_end."
    assert (period_start <= record_date <= period_end), "record_date must be >= period_start and <= period_end."
    
    
    num_days_in_period = days_between_dates(period_start, period_end)
    num_days_accrued = days_between_dates(period_start, pricing_date)
    
    daily_coupon_amount = coupon_payment_amount/num_days_in_period
    
    is_ex_coupon = pricing_date > record_date
    
    accrued_interest_amount = 0.00
    if is_ex_coupon:
        accrued_interest_amount = get_negative_accrued_interest(
            pricing_date,
            period_start,
            period_end,
            record_date + datetime.timedelta(days=1),
            coupon_payment_amount
        )
    else:
        accrued_interest_amount = num_days_accrued * daily_coupon_amount
        
    return accrued_interest_amount
    
def get_negative_accrued_interest(
    pricing_date: datetime.datetime,
    coupon_period_start_date = datetime.datetime,
    coupon_period_end_date = datetime.datetime,
    ex_date = datetime.datetime,
    coupon_payment_amount = float
) -> float:
    num_days_in_coupon_period = days_between_dates(coupon_period_start_date, coupon_period_end_date) + 1
    num_days_in_ex_period = days_between_dates(ex_date, coupon_period_end_date) + 1
    daily_accrual_amount = coupon_payment_amount / (num_days_in_coupon_period)
    total_negative_accrued = -1 * num_days_in_ex_period * daily_accrual_amount
    num_days_passed_in_ex_period = days_between_dates(ex_date, pricing_date)
    
    return total_negative_accrued + (daily_accrual_amount * num_days_passed_in_ex_period)

def get_pricing_history(
    issue_date: datetime.datetime,
    dirty_price_history: List[Dict],
    security_cashflow_input: List[Dict]
) -> List[Dict]:
    assert len(dirty_price_history) > 0, "dirty_price_history input must not be empty."
    assert len(security_cashflow_input) > 0, "security_cashflow_input must not be empty."
    
    start_of_first_period = issue_date
    
    pricing_history = []
    for price_dict in dirty_price_history:
        price_date = price_dict['date']
        price_value = price_dict['price']
        
        relevant_cashflow = None
        for i in range(0, len(security_cashflow_input)):
            if i == 0:
                cashflow_start = _default_date(start_of_first_period)
            else:
                previous_cashflow_payment_date = security_cashflow_input[i-1]['date']['payment_date']
                cashflow_start = _default_date(previous_cashflow_payment_date)
            
            cashflow_end = _default_date(security_cashflow_input[i]['date']['payment_date'])
            
            if cashflow_start <= price_date <= cashflow_end:
                relevant_cashflow = security_cashflow_input[i]
                break
        
        assert relevant_cashflow, f"Price date {price_dict} does not fall between {cashflow_start} and {cashflow_end}"
                
        cashflow_record_date = _default_date(relevant_cashflow['date']['record_date'])
        cashflow_payment_amount = relevant_cashflow['cashflow']['coupon_interest']['total_coupon_interest']
        accrued_interest = get_accrued_interest(
            price_date,
            cashflow_start,
            cashflow_end,
            cashflow_record_date,
            cashflow_payment_amount
        )
        
        pricing_history.append(
                {
                "date": price_date,
                "clean_price": price_value,
                "accrued_interest": accrued_interest,
                "dirty_price": price_value + accrued_interest
            }
        )
        
    return pricing_history
        
        
        