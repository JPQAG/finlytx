from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Dict, List

from src.analytics.utils.date_time import days_between_dates, months_between_dates, years_between_dates

def calculate_macaulay_duration(
    pricing_date: datetime,
    dirty_price: float,
    cashflows: List[Dict],
    yield_to_final: float 
) -> float:
    """Calculate the Macaulay duration of a security.

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
        float: The security's Macaulay Duration
    """
    days_between_coupon_dates = days_between_dates(cashflows[0].get("date"), cashflows[1].get("date"))
    # THis should be calculated by comparing pricing date to cashflow dates.
    ## Write function to get previous date in set of dates.
    lastCouponDate = cashflows[0]["date"] - relativedelta(days=days_between_coupon_dates)

    t = days_between_dates(lastCouponDate, pricing_date)
    T = days_between_dates(cashflows[0]["date"], cashflows[1]["date"])
    t_T = t/T
    FV = cashflows[-1]["cashflow_value"]
    r = yield_to_final
    N = years_between_dates(cashflows[0]["date"], cashflows[-1]["date"])

    numerator = 0
    denominator = dirty_price
    for i in range(1, N + 1):
        PMT = cashflows[i]["cashflow_value"]
        numerator += (((i-t_T)*PMT)/((1+r)**(N-t_T)))
       
    macaulay_duration = numerator / denominator

    return macaulay_duration
