import datetime
from typing import Dict

from src.analytics.utils.date_time import (
    _default_date
)

from src.analytics.utils.pricing import (
    get_security_currency_mapping
)

import datetime

def get_portfolio_valuation_index(
    portfolio_holdings_index: Dict,
    price_history_index: Dict        
) -> Dict:
    """Create a series of valuations for a set of holdings. Constructed from a holdings index.

    Args:
        portfolio_holdings_index (Dict): _description_
        price_history_index (Dict): _description_

    Raises:
        Exception: portfolio_holdings_index not dict type.
        Exception: price_hisotry_index not dict tpye.
        Execption: portfolio_holdings_index has no holdings before or on pricing_date input.

    Returns:
        Dict: _description_
    """
    assert portfolio_holdings_index, "portfolio_holdings_index input must not be empty."
    assert isinstance(portfolio_holdings_index, Dict), "portfolio_holdings_index input must be of type dict."
    assert isinstance(price_history_index, Dict), "price_history_index input must be of type dict."
    
    security_currency_mapping = get_security_currency_mapping(price_history_index)
    
    portfolio_valuation_index = {}
    
    for date, holdings in portfolio_holdings_index.items():
            
        prices_on_date_dict = _get_prices_on_date(_default_date(date), price_history_index)
        holdings_on_date_dict = holdings["holdings"]
        
        portfolio_valuation_index[date] = get_portfolio_valuation(
            _default_date(date),
            holdings_on_date_dict,
            prices_on_date_dict,
            security_currency_mapping
        )
    
    return portfolio_valuation_index

def get_portfolio_valuation(
    pricing_date: datetime.datetime,
    holdings: Dict,
    pricing: Dict,
    security_currency_mapping: Dict = {}
) -> Dict:
    assert isinstance(pricing_date, datetime.datetime), "pricing_date input must be of type datetime.datetime."
    assert isinstance(holdings, Dict), "holdings input must be of type dict."
    assert isinstance(pricing, Dict), "pricing input must be of type dict."
    assert holdings, "holdings must not be empty."
    
    no_price_available = {
        "date": datetime.datetime(2000,1,1),
        "per_original_face_value": -1.00,
        "currency": "N/A",
        "base_currency_conversion_rate": 1.00,
        "value": 0
    }
    
    portfolio_valuation = {
        "date": pricing_date,
        "valuation": {
            "total_valuation": {},
            "position_valuation": {}
        }
    }
    
    for security, holding in holdings.items():
        pricing_dict = pricing[security] if (security in pricing) else no_price_available
        pricing_dict['currency'] = security_currency_mapping[security] if (security in security_currency_mapping) else pricing_dict['currency']
        
        position_valuation = get_position_valuation(pricing_date, holding, pricing_dict)
        
        portfolio_valuation['valuation']['position_valuation'][security] = {
            "currency": pricing_dict['currency'],
            "volume": holding['volume'],
            "price": pricing_dict,
            "valuation": position_valuation
        }
        
        if pricing_dict['currency'] in portfolio_valuation['valuation']['total_valuation'] :
            portfolio_valuation['valuation']['total_valuation'][pricing_dict['currency']] += position_valuation
        else:
            portfolio_valuation['valuation']['total_valuation'][pricing_dict['currency']] = position_valuation
            
    return portfolio_valuation

def get_position_valuation(
    pricing_date: datetime.datetime,
    holding: Dict,
    price: Dict
) -> Dict:
    assert isinstance(pricing_date, datetime.datetime), "pricing_date input must be of type datetime.datetime."
    assert isinstance(holding, dict), "holding input must be of type dict."
    assert isinstance(price, dict), "price object input must be of type dict."
    assert pricing_date >= price['date'], "price object date must be on or before pricing date."
    assert holding, "Holdings dictionary cannot be empty."
    
    holding_valuation = holding['volume'] * price['value'] / price['per_original_face_value']
    
    return holding_valuation




def _get_prices_on_date(
    pricing_date: datetime.datetime,
    prices_history: Dict
) -> Dict:
    assert isinstance(pricing_date, datetime.datetime), "pricing_date must be a datetime object"
    assert isinstance(prices_history, dict), "prices_history must be a dictionary"
    for security, prices in prices_history.items():
        assert isinstance(security, str), f"{security} must be a string"
        assert isinstance(prices, dict), f"{prices} must be a dictionary"
        for date, price in prices.items():
            assert isinstance(date, str), f"{date} must be a string"
            assert isinstance(price, dict), f"{price} must be a dictionary"
            assert "date" in price, f"{price} must contain a 'date' key"
            assert "per_original_face_value" in price, f"{price} must contain a 'per_original_face_value' key"
            assert "currency" in price, f"{price} must contain a 'currency' key"
            assert "base_currency_conversion_rate" in price, f"{price} must contain a 'base_currency_conversion_rate' key"
            assert "value" in price, f"{price} must contain a 'value' key"
    
    prices_on_date = {}
    for security, prices in prices_history.items():
        price_dates = [date for date in prices.keys() if _default_date(date) <= pricing_date]
        
        prices_on_date[security] = prices[max(price_dates)] if price_dates else {}
                                
    return prices_on_date



