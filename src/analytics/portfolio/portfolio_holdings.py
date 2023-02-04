from typing import Dict, List
from operator import itemgetter
import copy

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
    securities = list(set(holding.keys() for date in holdings.values() for holding in date["holdings"].values()))
    
    holdings_delta_object = {
        "start_date": start_date,
        "end_date": end_date,
        "holdings_delta": {}
    }
    
    for security in securities:
        
        
        holdings_delta_object['holdings_delta'][security] = {
            "volume": 
        }