import copy
import datetime

from typing import Dict, List
from operator import itemgetter

from finx.analytics.utils.date_time import _default_date

def get_holdings_from_trades(
    trade_history: List[Dict]
) -> Dict:
    assert len(trade_history) > 0, "Trade history must not be empty."
    
    holdings_count = {}
    holdings_dict = {}
    
    for trade in trade_history:
        settlement_date, isin, side, volume = itemgetter("settlement_date", "isin", "side", "volume")(trade)
        assert (side == "B") or (side == "S"), "Side must be either 'B' or 'S'"
        net_volume = volume if side == "B" else volume * -1
        
        if isin in holdings_count.keys():
            holdings_count[isin]['volume'] += net_volume
        else:
            holdings_count[isin] = {}
            holdings_count[isin]['volume'] = net_volume
            
        
        
        holdings_dict[settlement_date] = {
            "date": settlement_date,
            "holdings": copy.deepcopy(holdings_count)
        }
        
    return holdings_dict

def get_holdings_delta(
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    holdings: Dict
) -> Dict:
    assert start_date < end_date, "Start date must be before end date."
    assert start_date.strftime('%Y-%m-%d') in holdings.keys(), "Start date must be in holdings."
    assert end_date.strftime('%Y-%m-%d') in holdings.keys(), "End date must be in holdings."
    
    assert isinstance(start_date, datetime.datetime), "Start date must be a datetime object."
    assert isinstance(end_date, datetime.datetime), "End date must be a datetime object."
    assert isinstance(holdings, dict), "Holdings must be a dictionary."
    
    assert len(holdings) > 0, "Holdings must not be empty."
    
    assert start_date.strftime('%Y-%m-%d') in holdings.keys(), "Start date must be in holdings."
    assert end_date.strftime('%Y-%m-%d') in holdings.keys(), "End date must be in holdings."
    
    securities = get_unique_securities_from_holdings(holdings)
    
    start_holdings = holdings[start_date.strftime('%Y-%m-%d')]["holdings"]
    start_holdings_securities = start_holdings.keys()
    
    end_holdings = holdings[end_date.strftime('%Y-%m-%d')]["holdings"]
    end_holdings_securities = end_holdings.keys()
        
    holdings_delta_object = {
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
        "holdings_delta": {}
    }
    
    for security in securities:
        
        start_holding_volume = start_holdings[security].get("volume", 0) if security in start_holdings_securities else 0
        end_holdings_volume = end_holdings[security].get("volume", 0) if security in end_holdings_securities else 0
        
        holdings_delta_object['holdings_delta'][security] = {
            "volume": end_holdings_volume - start_holding_volume
        } 
        
    return holdings_delta_object
        
def get_unique_securities_from_holdings(
    holdings: Dict
) -> List:
    assert isinstance(holdings, dict), "Holdings must be a dictionary."
    assert len(holdings) > 0, "Holdings must not be empty."
    
    security_list = []
    
    for security in holdings.values():
        
        for security in security["holdings"].keys():
            
            if security not in security_list:
                security_list.append(security)
                
    return security_list


def get_dict_from_trade_list(
    trades: List[Dict]
) -> Dict:
    
    trade_dict = {}
    trade_dates = list(set([trade['trade_date'] for trade in trades]))
    
    for trade_date in trade_dates:
        trades_on_date = [trade for trade in trades if trade['trade_date'] == trade_date]
        trade_dict[trade_date] = trades_on_date
        
    return trade_dict
    
def get_invested_capital_delta(
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    trades: List
) -> Dict:
    """
        Calculates the change in invested capital for a given date range.

        The function takes in a start date, end date and a dictionary of trades as inputs. 
        The start date and end date define the date range for which the change in invested capital is to be calculated. 
        The trades dictionary contains details of trades such as settlement date, current face value, volume, price, side and ISIN.

        The function returns a dictionary with the invested capital delta for each unique security traded in the given date range. 
        A trade is considered in the calculation only if its settlement date falls between the start and end dates (inclusive).

        The invested capital delta is calculated as the product of the volume, price and the side of the trade, 
        divided by the current face value (default value is 100 if current face value is not available). 
        If the trade is a buy, the delta is positive. If the trade is a sell, the delta is negative.

        Parameters:
            start_date (datetime.datetime): The start date of the date range.
            end_date (datetime.datetime): The end date of the date range.
            trades (Dict): A dictionary of trades, containing details such as settlement date, current face value, volume, price, side and ISIN.

        Returns:
        Dict: A dictionary with the invested capital delta for each unique security traded in the given date range. The dictionary contains a start date, end date and a nested dictionary for invested capital delta for each security.

        Example:
        trades = [{'settlement_date': '2022-01-01', 'current_face_value': 100, 'volume': 10, 'price': 100, 'side': 'B', 'isin': 'ABC123'},
                {'settlement_date': '2022-02-01', 'current_face_value': 100, 'volume': 20, 'price': 110, 'side': 'S', 'isin': 'ABC123'},
                {'settlement_date': '2022-03-01', 'current_face_value': 90, 'volume': 5, 'price': 120, 'side': 'B', 'isin': 'XYZ456'}]
        start_date = datetime.datetime(2022, 1, 1)
        end_date = datetime.datetime(2022, 2, 28)
        invested_capital_delta = get_invested_capital_delta(start_date, end_date, trades)
        print(invested_capital_delta)
        # Output:
        # {'start_date': '2022-01-01',
        #  'end_date': '2022-02-28',
        #  'invested_capital_delta': {'ABC123': {'volume': 1000.0},
        #                             'XYZ456': {'volume': 0}}}
    """
    traded_securities = get_unique_securities_from_trades(trades)
    
    invested_capital_delta = {
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
        "invested_capital_delta": {security: {'volume': 0} for security in traded_securities}
    }
    
    for trade in trades:
        if not (start_date <= _default_date(trade['settlement_date']) <= end_date):
            continue
        
        face_value = trade['current_face_value'] if trade['current_face_value'] else 100
        
        delta = (trade['volume'] * trade['price'] / face_value) if trade['side'] == 'B' else (trade['volume'] * trade['price'] / face_value * -1)
        
        invested_capital_delta['invested_capital_delta'][trade['isin']]['volume'] += delta
        
    return invested_capital_delta

        
def get_unique_securities_from_trades(
    trades: List
) -> List:
    assert isinstance(trades, List), "Trades must be a list."
    assert len(trades) > 0, "Trades must not be empty."
     
    return list(set([trade['isin'] for trade in trades]))    

def get_holdings_by_date_and_currency(
    holdings: Dict,
    security_currency_map: Dict
) -> Dict:
    assert isinstance(holdings, dict), "Holdings must be a dictionary."
    assert len(holdings) > 0, "Holdings must not be empty."
    assert isinstance(security_currency_map, dict), "Security currency map must be a dictionary."
    
    holdings_securities = get_unique_securities_from_holdings(holdings)
    assert all([security in security_currency_map.keys() for security in holdings_securities]), "Security currency map must contain all securities in holdings."
    
    holdings_by_date_and_currency = {}
    
    for date, holdings_on_date in holdings.items():
        holdings_by_date_and_currency[date] = {}
        
        for security, holding in holdings_on_date['holdings'].items():
            currency = security_currency_map[security]
            holdings_by_date_and_currency[date][currency] = holdings_by_date_and_currency[date].get(currency, 0) + holding['volume']
    
    return holdings_by_date_and_currency