import datetime
from typing import Dict, List, Tuple

from src.analytics.utils.date_time import (
    _default_date
)

def get_portfolio_future_cashflows(
    portfolio_holdings: Dict,
    security_cashflows_object: Dict,
    key_mapping: List[Tuple[str, str]] = [
        ('total', 'total'),
        ('fixed_coupon_interest_component', 'coupon_interest.fixed_coupon_interest_component'),
        ('variable_coupon_interest_component', 'coupon_interest.variable_coupon_interest_component'),
        ('total_coupon_interest', 'coupon_interest.total_coupon_interest'),
        ('redemption_principal', 'principal.redemption_principal'),
        ('amortising', 'principal.amortising'),
        ('total_principal', 'principal.total_principal'),
    ]
) -> Dict:
    """Calculates a portfolio's future cashflows given current holdings and the 
        cashflow profiles of those holdings.
        
    * Uses the portfolio holdings date attribute as the effective pricing date.

    Args:
        portfolio_holdings (Dict): A dictionary containing the portfolio holdings and the effective pricing date.
        security_cashflows_object (Dict): A dictionary containing the cashflow profiles of the securities in the portfolio.
        key_mapping (List[Tuple[str, str]]): A list of tuples mapping the keys in the portfolio_holdings dictionary to the keys in the security_cashflows_object dictionary. Default is [('total', 'total'), ('fixed_coupon_interest_component', 'coupon_interest.fixed_coupon_interest_component'), ('variable_coupon_interest_component', 'coupon_interest.variable_coupon_interest_component'), ('total_coupon_interest', 'coupon_interest.total_coupon_interest'), ('redemption_principal', 'principal.redemption_principal'), ('amortising', 'principal.amortising'), ('total_principal', 'principal.total_principal')].
    ```
    Returns:
            Dict: A dictionary containing the future cashflows for each security in the portfolio.
    """
    assert isinstance(portfolio_holdings, Dict), "portfolio_holdings input must be of type Dict."
    assert isinstance(security_cashflows_object, Dict), "security_cashflows_object input must be of type Dict."
    assert portfolio_holdings, "portfolio_holdings input must not be empty."
    assert security_cashflows_object, "security_cashflows_object input must not be empty."
    assert isinstance(key_mapping, list), "key_mapping input must be of type list."
    assert all(isinstance(key_tuple, tuple) and len(key_tuple) == 2 for key_tuple in key_mapping), "key_mapping input must be a list of tuples, each tuple containing two strings."
    
    pricing_date = _default_date(portfolio_holdings["date"])
    portfolio_holdings_map = {id: info["volume"] for id, info in portfolio_holdings["holdings"].items()}
    
    portfolio_future_cashflows = {}
    
    for security, security_cashflows in security_cashflows_object.items():
        
        for date, cashflow in security_cashflows.items():
            
            if _default_date(date) < pricing_date:
                continue
            
            portfolio_future_cashflows[date] = {}
            
            volume_multiplier = portfolio_holdings_map[security] / 100.00
            
            for key_tuple in key_mapping:
                portfolio_key, cashflow_key = key_tuple
                if cashflow_key == 'total':
                    cashflow['cashflow'][cashflow_key] *= volume_multiplier
                else:
                    key_path = cashflow_key.split('.')
                    cashflow['cashflow'][key_path[0]][key_path[1]] *= volume_multiplier
            
            portfolio_future_cashflows[date][security] = cashflow
            
    portfolio_future_cashflows = {k: v for k, v in sorted(portfolio_future_cashflows.items(), key=lambda item: _default_date(item[0]))}
            
    return portfolio_future_cashflows