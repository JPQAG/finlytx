import datetime
from typing import Any, Dict, List
import pandas as pd

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
            
            cashflow_end = _default_date(security_cashflow_input[i]['date']['payment_date']) - datetime.timedelta(days=1)
            
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
                "date": pd.to_datetime(price_date).strftime("%Y-%m-%d"),
                "clean_price": price_value,
                "accrued_interest": accrued_interest,
                "dirty_price": price_value + accrued_interest
            }
        )
        
    return pricing_history

def get_period_total_return(
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    price_history: List[Dict],
    security_cashflows: List[Dict]
) -> float:
    assert all([isinstance(date, datetime.datetime) for date in [start_date, end_date]]), f"{start_date} and {end_date} must be of type datetime."

    cashflows_paid = [
        cashflow for cashflow
        in security_cashflows
        if start_date <= _default_date(cashflow['date']['record_date']) <= end_date
    ]
    cashflow_payment_sum = sum(cashflow['cashflow']['total'] for cashflow in cashflows_paid)
    
    relevant_price_dates = [
        price_dict for price_dict
        in price_history
        if start_date.date() <= _default_date(price_dict['date']).date() <= end_date.date()
    ]
    
    assert len(relevant_price_dates) > 1, "price_history must be greater than a single day."
    start_date_price_dict = relevant_price_dates[0]
    end_date_price_dict = relevant_price_dates[-1]
    
    price_return = (end_date_price_dict['price'] - start_date_price_dict['price']) / start_date_price_dict['price']
    cashflow_return = cashflow_payment_sum / start_date_price_dict['price']
    total_return = price_return + cashflow_return
    
    return_profile = {
        'return': {
            'price_return': price_return,
            'cashflow_return': cashflow_return,
            'total_return': total_return
        },
        'cashflows_paid': cashflows_paid,
        'relevant_price_dates': relevant_price_dates        
    }
    
    return return_profile

def get_annualised_return(
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    cumulative_return: List[Dict],
    days_in_year: float=365
) -> float:
    number_of_days_held = days_between_dates(start_date, end_date)
    
    annualised_return = (((1+cumulative_return)**(days_in_year/number_of_days_held)) - 1)
    
    return annualised_return
    
        
        