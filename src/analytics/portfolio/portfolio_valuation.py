from typing import Dict

from src.analytics.utils.date_time import (
    _default_date
)

def get_portfolio_valuation(
    security_des_index: Dict,
    portfolio_holdings_index: Dict,
    price_history_index: Dict        
) -> Dict:
    assert all(
        [security_des_index, portfolio_holdings_index, price_history_index]
    ), "Input indices cannot be empty."

## CHECK ALL PRICE HISTORYS INCLUDED
