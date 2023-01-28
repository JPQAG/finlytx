import datetime
from typing import Dict

from src.analytics.utils.date_time import (
    _default_date
)

def get_portfolio_performance_index(
    pricing_date: datetime.datetime,
    holdings: Dict,
    cashflows: Dict,
    prices: Dict
) -> Dict:
    """Get the portfolio performance between two dates where there is unchanged holdings.
    """
    assert isinstance(pricing_date, datetime.datetime), "pricing_date input must be of type datetime.datetime."
    assert isinstance(holdings, dict), "holdings input must be of type dict."
    assert isinstance(cashflows, dict), "cashflows input must be of type dict."
    assert isinstance(prices, dict), "prices input must be of type dict."
    assert len(holdings) > 0, "holdings input must not be empty."
    assert len(cashflows) > 0, "cashflows input must not be empty."
    assert len(prices) > 0, "prices input must not be empty."

def get_portfolio_performance():
    """Get the portfolio performance between two dates as a change in dollar value (valuation change + cashflow).
    
    # Add/subtract change in valuation
    # Add/subtract income
    # Add/subtract capital in/out of portfolio (net consideration of buys/sells)
    
    # *Security redemption treated as a sale
    
    """
    pass
    
    

