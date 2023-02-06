from typing import Dict, List
from operator import itemgetter
import copy
import datetime

from src.analytics.utils.date_time import (
    _default_date
)

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
    
    for trade in trades:
        trade_dict[trade['trade_date']] = trade
        
    return trade_dict
    
def get_invested_capital_delta(
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    trades: Dict
) -> Dict:
    traded_securities = get_unique_securities_from_trades(trades)
    
    invested_capital_delta = {
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
        "invested_capital_delta": {security: {'volume': 0} for security in traded_securities}
    }
    
    for trade in trades.values():
        if not (start_date <= _default_date(trade['settlement_date']) <= end_date):
            continue
        
        delta = trade['volume'] * trade['price'] if trade['side'] == 'B' else trade['volume'] * trade['price'] * -1
        
        invested_capital_delta['invested_capital_delta'][trade['isin']]['volume'] += delta
        
    return invested_capital_delta

        
def get_unique_securities_from_trades(
    trades: Dict
) -> List:
    assert isinstance(trades, dict), "Trades must be a dictionary."
    assert len(trades) > 0, "Trades must not be empty."
    
    securities = []
    
    for trade in trades.values():
        
        if trade['isin'] not in securities:
            securities.append(trade['isin'])
            
    return securities
    
    