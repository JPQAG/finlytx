import datetime
from typing import Dict, List

from src.analytics.utils.date_time import (
    _default_date
)

from src.analytics.portfolio.portfolio_holdings import (
    get_invested_capital_delta,
    get_holdings_by_date_and_currency
)

from src.analytics.portfolio.portfolio_cashflows import (
    get_portfolio_historical_cashflows,
    get_performance_period_cashflow_income
)

from src.analytics.portfolio.portfolio_valuation import (
    get_portfolio_valuation_index
)

from src.analytics.utils.pricing import (
    get_unique_currencies,
    get_security_currency_mapping
)

def get_portfolio_performance_index(
    pricing_date: datetime.datetime,
    trades: List,
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
    assert isinstance(trades, List), "trades input must be of type list."
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
    performance_index = {"start_date": holdings_dates[0],"end_date": pricing_date.strftime('%Y-%m-%d'),"index": {}}
    portfolio_valuation_index = get_portfolio_valuation_index(
        holdings,
        prices
    )
    security_currency_map = get_security_currency_mapping(prices)
    holdings_by_date_and_currency = get_holdings_by_date_and_currency(holdings, security_currency_map)
    
    
    for i in range(0, len(holdings_dates) - 1):
        performance_index['index'][holdings_dates[i]] = {
            "date": holdings_dates[i],
            "index_values": {},
            "performance_since_last": {
                "valuation_change": {},
                "cashflow_income": {},
                "invested_capital_delta": {}
            }
        }

        if i == 0:    
            for currency in unique_currencies:
                performance_index['index'][holdings_dates[i]]['index_values'][currency] = starting_index_value        
            continue
        
        starting_date = holdings_dates[i - 1]
        ending_date = holdings_dates[i]
        
        index_at_start = performance_index['index'][holdings_dates[i - 1]]['index_values']
        
        valuation_change_by_currency = {}
        period_performance = get_portfolio_performance(
            pricing_date,
            portfolio_valuation_index[starting_date],
            portfolio_valuation_index[ending_date],
            prices,
            cashflows,
            holdings
        )
        for currency in unique_currencies:
            valuation_change_by_currency[currency] = period_performance['investment_value_change']['valuation_change'][currency]
        
        
        invested_capital_delta_by_currency = {}
        invested_capital_delta_by_security = get_invested_capital_delta(
            _default_date(starting_date) + datetime.timedelta(days=1),
            _default_date(ending_date),
            trades
        )
        for currency in unique_currencies:
            securities_in_currency = [security for security in security_currency_map if security_currency_map[security] == currency]
            invested_capital_delta_by_currency[currency] = sum([invested_capital_delta_by_security['invested_capital_delta'][security]['volume'] for security in securities_in_currency])       
        
        income_by_currency = get_performance_period_cashflow_income(
            _default_date(starting_date),
            _default_date(ending_date),
            period_performance['investment_value_change']['cashflow_income'],
            security_currency_map
        )
                
        for currency in unique_currencies:
            if currency not in holdings_by_date_and_currency[starting_date].keys() or holdings_by_date_and_currency[starting_date][currency] == 0:
                performance_index['index'][holdings_dates[i]]['index_values'][currency] = performance_index['index'][holdings_dates[i - 1]]['index_values'][currency]
                performance_index['index'][holdings_dates[i]]['performance_since_last']['valuation_change'][currency] = 0
                performance_index['index'][holdings_dates[i]]['performance_since_last']['cashflow_income'][currency] = 0
                performance_index['index'][holdings_dates[i]]['performance_since_last']['invested_capital_delta'][currency] = 0
            else:    
                income = income_by_currency[currency] if currency in income_by_currency.keys() else 0
                valuation_change = valuation_change_by_currency[currency] if currency in valuation_change_by_currency.keys() else 0
                invested_capital_change = invested_capital_delta_by_currency[currency] if currency in invested_capital_delta_by_currency.keys() else 0
                
                starting_valuation = portfolio_valuation_index[starting_date]["valuation"]["total_valuation"][currency]
                
                    
                total_investment_change = valuation_change + income - invested_capital_change
                period_performance_percentage = total_investment_change / starting_valuation
                ending_index_value = index_at_start[currency] * (1 + period_performance_percentage)            
                
                performance_index['index'][holdings_dates[i]]['index_values'][currency] = ending_index_value
                performance_index['index'][holdings_dates[i]]['performance_since_last']['valuation_change'][currency] = valuation_change
                performance_index['index'][holdings_dates[i]]['performance_since_last']['cashflow_income'][currency] = income
                performance_index['index'][holdings_dates[i]]['performance_since_last']['invested_capital_delta'][currency] = invested_capital_change
                
    return performance_index
          
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
        'start_date': start_valuation['date'].strftime("%Y-%m-%d"),
        'end_date': end_valuation['date'].strftime("%Y-%m-%d"),
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
    
    start_date = start_valuation['date']
    start_val = start_valuation['valuation'].get('total_valuation', {})
    end_date = end_valuation['date']
    end_val = end_valuation['valuation'].get('total_valuation', {})
    currencies = list(set(start_val.keys()) | set(end_val.keys()))
        
    portfolio_valuation_difference = {
        "valuation_change": {}
    }
    
    for currency in currencies:
        start_valuation_value = start_val.get(currency, 0)
        end_valuation_value = end_val.get(currency, 0)
        portfolio_valuation_difference['valuation_change'][currency] = end_valuation_value - start_valuation_value
            
    return portfolio_valuation_difference
