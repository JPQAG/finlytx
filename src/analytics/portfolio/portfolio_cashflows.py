import datetime
from typing import Dict, List, Tuple
import copy

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
    * Includes only cashflows that have not yet reached their record ex date.

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
            
            ex_coupon_date = _default_date(cashflow['date']['ex_date'])
            payment_date = _default_date(cashflow['date']['payment_date'])
            if ex_coupon_date < pricing_date < payment_date:
                continue
            
            if _default_date(date) < pricing_date:
                continue
            
            portfolio_future_cashflows[date] = {} if date not in portfolio_future_cashflows else portfolio_future_cashflows[date]
                                    
            portfolio_future_cashflows[date][security] = _get_cashflow_given_holdings(
                cashflow,
                security,
                portfolio_holdings,
                key_mapping
            )
            
    portfolio_future_cashflows = {k: v for k, v in sorted(portfolio_future_cashflows.items(), key=lambda item: _default_date(item[0]))}
            
    return portfolio_future_cashflows


def get_portfolio_historical_cashflows(
    pricing_date: datetime.datetime,
    portfolio_holdings_index: Dict,
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
    """Calculates a portfolio's historical cashflows given current holdings and the 
        cashflow profiles of those holdings.
        
    * Uses the portfolio holdings date attribute as the effective pricing date.

    Args:
        portfolio_holdings_index (Dict): A dictionary containing the portfolio holdings and the effective pricing date.
        security_cashflows_object (Dict): A dictionary containing the cashflow profiles of the securities in the portfolio.
    ```
    Returns:
        Dict: A dictionary containing the historical cashflows for the portfolio by date.
    """
    assert isinstance(portfolio_holdings_index, Dict), "portfolio_holdings_index input must be of type Dict."
    assert isinstance(security_cashflows_object, Dict), "security_cashflows_object input must be of type Dict."
    assert portfolio_holdings_index, "portfolio_holdings_index input must not be empty."
    assert security_cashflows_object, "security_cashflows_object input must not be empty."
    
    holdings_dates = [date for date in portfolio_holdings_index.keys()]
    ordered_holdings_dates = sorted(holdings_dates, key=lambda date: _default_date(date))
        
    portfolio_historical_cashflows = {}

    for i in range(0, len(ordered_holdings_dates)):
        
        holdings_date = _default_date(ordered_holdings_dates[i])
        next_holdings_date = _default_date(ordered_holdings_dates[i+1]) if i+1 < len(ordered_holdings_dates) else datetime.datetime.max
        
        holdings_at_date = portfolio_holdings_index[ordered_holdings_dates[i]]['holdings']
        
        for security_id, holdings_info in holdings_at_date.items():
            
            # if holdings volume zero then continue
            if holdings_info['volume'] == 0:
                continue
            
            security_cashflows = security_cashflows_object[security_id]
            
            for date, cashflow in security_cashflows.items():
                
                ex_coupon_date = _default_date(cashflow['date']['ex_date'])
                coupon_payment_date = _default_date(cashflow['date']['payment_date'])
                
                if not (holdings_date < ex_coupon_date < next_holdings_date) or (coupon_payment_date >= pricing_date):
                    continue
                                
                if date not in portfolio_historical_cashflows:
                    portfolio_historical_cashflows[date] = {}
                
                portfolio_historical_cashflows[date][security_id] = _get_cashflow_given_holdings(
                    cashflow,
                    security_id,
                    portfolio_holdings_index[ordered_holdings_dates[i]],
                    key_mapping
                )
    
    portfolio_historical_cashflows = {k: v for k, v in sorted(portfolio_historical_cashflows.items(), key=lambda item: _default_date(item[0]))}
    
    return portfolio_historical_cashflows


def _get_cashflow_given_holdings(
    cashflow: Dict,
    security_id: str,
    holdings: Dict,
    key_mapping: List[Tuple[str, str]]
) -> Dict:
    """Calculates the cashflow for a security given the current holdings.
    
    Args:
        cashflow (Dict): A dictionary containing the cashflow profile of a security.
        security_id (Dict): A string containing the security id.
        holdings (Dict): A dictionary containing the current holdings of a security.
        key_mapping (List[Tuple[str, str]]): A list of tuples containing the keys to map from the cashflow profile to the holdings.
    ```
    Returns:
        Dict: A dictionary containing the cashflow for a security given the current holdings.
    """
    assert isinstance(cashflow, Dict), "cashflow input must be of type Dict."
    assert isinstance(holdings, Dict), "holdings input must be of type Dict."
    assert isinstance(key_mapping, List), "key_mapping input must be of type List."
    assert all(isinstance(key_tuple, Tuple) and len(key_tuple) == 2 for key_tuple in key_mapping), "key_mapping input must be a list of tuples, each tuple containing two strings."
    assert cashflow, "cashflow input must not be empty."
    assert holdings, "holdings input must not be empty."
    
    cashflow = copy.deepcopy(cashflow)
        
    security_holdings_volume = holdings['holdings'][security_id]['volume']
    
    volume_multiplier = security_holdings_volume / 100.00
            
    for key_tuple in key_mapping:
        portfolio_key, cashflow_key = key_tuple
        if cashflow_key == 'total':
            cashflow['cashflow'][cashflow_key] *= volume_multiplier
        else:
            key_path = cashflow_key.split('.')
            cashflow['cashflow'][key_path[0]][key_path[1]] *= volume_multiplier
    
    return cashflow
                
                
def get_performance_period_cashflow_income(
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    cashflow_income: Dict,
    security_currency_map: Dict
) -> float:
    """Calculates the cashflow income for a given performance period.
    
    Args:
        start_date (datetime.datetime): A datetime object containing the start date of the performance period.
        end_date (datetime.datetime): A datetime object containing the end date of the performance period.
        cashflow_income (Dict): A dictionary containing the cashflow income for a portfolio.
    ```
    Returns:
        float: A float containing the cashflow income for a given performance period.
    """
    assert isinstance(start_date, datetime.datetime), "start_date input must be of type datetime.datetime."
    assert isinstance(end_date, datetime.datetime), "end_date input must be of type datetime.datetime."
    assert isinstance(cashflow_income, Dict), "cashflow_income input must be of type Dict."
    assert cashflow_income, "cashflow_income input must not be empty."
    
    performance_period_cashflow_income = {}
    
    for date, security_cashflows in cashflow_income.items():
        if start_date <= _default_date(date) <= end_date:
            for isin, cashflow in security_cashflows.items():
                currency = security_currency_map[isin]
                performance_period_cashflow_income[currency] = performance_period_cashflow_income.get(currency, 0.00)
                performance_period_cashflow_income[currency] += cashflow['cashflow']['total']
    
    return performance_period_cashflow_income

