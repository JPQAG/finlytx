import datetime
from typing import Dict

from src.analytics.utils.date_time import (
    _default_date
)

def get_portfolio_valuation_index(
    pricing_date: datetime.datetime,
    portfolio_holdings_index: Dict,
    price_history_index: Dict        
) -> Dict:
    assert isinstance(portfolio_holdings_index, Dict), "portfolio_holdings_index input must be of type dict."
    assert isinstance(price_history_index, Dict), "price_history_index input must be of type dict."
    assert portfolio_holdings_index, "portfolio_holdings_index input must not be empty."
    
    
    
    return 0

def get_portfolio_valuation(
    pricing_date: datetime.datetime,
    holdings: Dict,
    pricing: Dict
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
