import datetime
from typing import Dict

from src.analytics.utils.date_time import (
    _default_date
)

from typing import Dict
import datetime

def get_portfolio_valuation_index(
    pricing_date: datetime.datetime,
    portfolio_holdings_index: Dict,
    price_history_index: Dict        
) -> Dict:
    # Check if portfolio_holdings_index is a dictionary
    if not isinstance(portfolio_holdings_index, Dict):
        raise Exception("portfolio_holdings_index input must be of type dict.")
        
    # Check if price_history_index is a dictionary
    if not isinstance(price_history_index, Dict):
        raise Exception("price_history_index input must be of type dict.")
    
    # Initialize empty portfolio_valuation_index
    portfolio_valuation_index = {}
    
    # Iterate over dates in portfolio_holdings_index
    for date, holdings in portfolio_holdings_index.items():
        # Convert date to datetime
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        
        # Check if date is before valuation date
        if date < pricing_date:
            # Initialize empty valuation for this date
            valuation = 0
            
            # Iterate over securities in holdings
            for security, data in holdings['holdings'].items():
                # Check if security is present in price_history_index
                if security not in price_history_index:
                    raise Exception("No price data found for securities in portfolio at valuation date.")
                
                # Check if there is a price for the security on the valuation date
                if pricing_date.strftime('%Y-%m-%d') not in price_history_index[security]:
                    raise Exception("No price data found for securities in portfolio at valuation date.")
                
                # Calculate valuation for this security
                security_valuation = get_position_valuation(security, data, price_history_index)
                
                # Add valuation for this security to total valuation
                valuation += security_valuation
            
            # Add valuation for this date to portfolio_valuation_index
            portfolio_valuation_index[date.strftime('%Y-%m-%d')] = valuation
    
    return portfolio_valuation_index


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
