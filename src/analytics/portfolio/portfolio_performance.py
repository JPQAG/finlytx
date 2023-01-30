import datetime
from typing import Dict

from src.analytics.utils.date_time import (
    _default_date
)

from src.analytics.portfolio.portfolio_cashflows import (
    get_portfolio_historical_cashflows
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

def get_portfolio_performance(
    pricing_date: datetime.datetime,
    start_valuation: Dict,
    end_valuation: Dict,
    prices: Dict,
    cashflows: Dict,
    holdings: Dict
) -> Dict:
    """Get the portfolio performance between two dates as a change in dollar value (valuation change and cashflow_income).
    
    # Add/subtract change in valuation
    # Add/subtract income
    # Add/subtract capital in/out of portfolio (net consideration of buys/sells)
    
    # *Security redemption treated as a sale
    
    Args:
        pricing_date (datetime.datetime): The date of the valuation.
        start_valuation (Dict): The start valuation of the portfolio.
        end_valuation (Dict): The end valuation of the portfolio.
        prices (Dict): The prices of the securities in the portfolio.
        cashflows (Dict): The cashflows of the securities in the portfolio.
        hodlings (Dict): The trades of the securities in the portfolio.
        
    Raises:
        Exception: If the pricing_date is not of type datetime.datetime.
        Exception: If the start_valuation is not of type dict.
        Exception: If the end_valuation is not of type dict.
        Exception: If the prices is not of type dict.
        Exception: If the cashflows is not of type dict.
        Exception: If the trades is not of type dict.
    
    Returns:
        Dict: The portfolio performance dictionary containing valuation_change and cashflow_income.
    
    """
    assert isinstance(pricing_date, datetime.datetime), "pricing_date input must be of type datetime.datetime."
    assert isinstance(start_valuation, dict), "start_valuation input must be of type dict."
    assert isinstance(end_valuation, dict), "end_valuation input must be of type dict."
    assert isinstance(prices, dict), "prices input must be of type dict."
    assert isinstance(cashflows, dict), "cashflows input must be of type dict."
    assert isinstance(holdings, dict), "holdings input must be of type dict."
    
    assert len(start_valuation) > 0, "start_valuation input must not be empty."
    assert len(end_valuation) > 0, "end_valuation input must not be empty."
    assert len(prices) > 0, "prices input must not be empty."
    assert len(cashflows) > 0, "cashflows input must not be empty."
    assert len(holdings) > 0, "holdings input must not be empty."
    
    portfolio_performance = {
        'pricing_date': pricing_date,
        'start_date': start_valuation['valuation_date'],
        'end_date': end_valuation['valuation_date']
    }
    
    portfolio_performance['investment_value_change'] = {}
    portfolio_performance['investment_value_change']['valuation_change'] = get_portfolio_valuation_difference(
        start_valuation,
        end_valuation
    )
    portfolio_performance['investment_value_change']['cashflow_income'] = get_portfolio_historical_cashflows(
        pricing_date,
        holdings,
        cashflows
    )
    
    return portfolio_performance

def get_portfolio_valuation_difference(
    start_valuation: Dict,
    end_valuation: Dict
) -> Dict:
    """Get the difference between two portfolio valuations.
    
    Args:
        start_valuation (Dict): The start valuation of the portfolio.
        end_valuation (Dict): The end valuation of the portfolio.
        
    Raises:
        Exception: If the start_valuation is not of type dict.
        Exception: If the end_valuation is not of type dict.
    
    Returns:
        Dict: The portfolio valuation difference dictionary.
    
    """
    assert isinstance(start_valuation, dict), "start_valuation input must be of type dict."
    assert isinstance(end_valuation, dict), "end_valuation input must be of type dict."
    
    assert len(start_valuation) > 0, "start_valuation input must not be empty."
    assert len(end_valuation) > 0, "end_valuation input must not be empty."
    
    portfolio_valuation_difference = {}
    
    start_date = start_valuation['valuation_date']
    start_val = start_valuation[start_date].get('valuation', 0)
    end_date = end_valuation['valutaion_date']
    end_val = end_valuation[end_date].get('valuation', 0)
    currencies = list(set(start_val.keys()) | set(end_val.keys()))
        
    portfolio_valuation_difference = {
        "start_date": start_date,
        "end_date": end_date,
        "valuation_change": {
            "date": "2001-01-01",
            "valuation": {}
        }
    }
    
    for currency in currencies:
        portfolio_valuation_difference['valuation_change']['valuation'][currency] = end_val[currency] - start_val[currency]
            
    return portfolio_valuation_difference
