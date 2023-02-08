import datetime
from typing import Dict

from src.analytics.utils.date_time import (
    _default_date
)

from src.analytics.portfolio.portfolio_holdings import (
    get_invested_capital_delta   
)

from src.analytics.portfolio.portfolio_cashflows import (
    get_portfolio_historical_cashflows,
    get_performance_period_cashflow_income
)

from src.analytics.portfolio.portfolio_valuation import (
    get_portfolio_valuation_index
)

from src.analytics.utils.pricing import (
    get_unique_currencies
)

def get_portfolio_performance_index(
    pricing_date: datetime.datetime,
    trades: Dict,
    holdings: Dict,
    cashflows: Dict,
    prices: Dict,
) -> Dict:
    """Create an index representing the change in value from a base value from the first to last holding date.
    
    ** Change in index is the change in valuation plus the change in cashflow between two dates.
    ** Currency Conversion/enhancement done at a higher level? Keep currencies separate?
        ** Valuation, cashflow and investment changes are all separated by currency.
        ** Therefore there is an index for each currency.
        ** All indices start at 100 on the first holdings date.
    
    * Start at first holdings date. Finish at pricing_date
    * get portfolio performance between each 
    * Include cashflows between each holdings date.
    
    
    """
    assert isinstance(pricing_date, datetime.datetime), "pricing_date input must be of type datetime.datetime."
    assert isinstance(trades, dict), "trades input must be of type dict."
    assert isinstance(holdings, dict), "holdings input must be of type dict."
    assert isinstance(cashflows, dict), "cashflows input must be of type dict."
    assert isinstance(prices, dict), "prices input must be of type dict."
    assert len(holdings) > 0, "holdings input must not be empty."
    assert len(trades) > 0, "trades input must not be empty."
    assert len(cashflows) > 0, "cashflows input must not be empty."
    assert len(prices) > 0, "prices input must not be empty."
    
    starting_index_value = 100
    holdings_dates = list(holdings.keys())
    unique_currencies = get_unique_currencies(prices)
    performance_index = {
        "start_date": holdings_dates[0],
        "end_date": pricing_date,
        "index": {}
    }
    portfolio_valuation_index = get_portfolio_valuation_index(
        holdings,
        prices
    )
    
    
    for i in range(0, len(holdings_dates) - 1):
        starting_date = holdings_dates[i]
        ending_date = holdings_dates[i + 1]
        
        if i == 0:
            performance_index['index'][holdings_dates[i]] = {
                "date": holdings_dates[i],
                "index_values": {},
                "performance_since_last": {}
            }
            
            for currency in unique_currencies:
                performance_index['index'][holdings_dates[i]]['index_values'][currency] = starting_index_value
                
            continue
        
        valuation_at_start = portfolio_valuation_index[starting_date]
        valuation_at_end = portfolio_valuation_index[ending_date]
        index_at_start = performance_index['index'][holdings_dates[i - 1]]['index_values']
        
        invested_capital_delta = get_invested_capital_delta(
            _default_date(starting_date) + datetime.timedelta(days=1),
            _default_date(ending_date),
            trades
        )
        
        period_performance = get_portfolio_performance(
            pricing_date=pricing_date,
            start_valuation=valuation_at_start,
            end_valuation=valuation_at_end,
            prices=prices,
            cashflows=cashflows,
            holdings=holdings
        )
        
        income = get_performance_period_cashflow_income(
            starting_date,
            ending_date,
            period_performance['investment_value_change']['cashflow_income']
        )
        
        for currency in unique_currencies:
            valuation_change = period_performance['investment_value_change']['valuation_change'][currency]
        
        # performance_index['index'][holdings_dates[i]]['index_values'][currency] = 
        
        #INCOME CURRENCY NEEDS TO BE SPLIT OUT?
        

          
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
        'pricing_date': pricing_date.strftime("%Y-%m-%d"),
        'start_date': start_valuation['valuation_date'],
        'end_date': end_valuation['valuation_date']
    }
    
    portfolio_performance['investment_value_change'] = {}
    portfolio_performance['investment_value_change'] = get_portfolio_valuation_difference(
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
    start_val = start_valuation.get('total_valuation', {})
    end_date = end_valuation['valuation_date']
    end_val = end_valuation.get('total_valuation', {})
    currencies = list(set(start_val.keys()) | set(end_val.keys()))
        
    portfolio_valuation_difference = {
        "valuation_change": {}
    }
    
    for currency in currencies:
        start_valuation_value = start_val.get(currency, 0)
        end_valuation_value = end_val.get(currency, 0)
        portfolio_valuation_difference['valuation_change'][currency] = end_valuation_value - start_valuation_value
            
    return portfolio_valuation_difference
