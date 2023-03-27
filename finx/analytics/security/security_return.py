from typing import Dict, List

def get_period_return(
    previous_close_price: float,
    close_price: float
) -> float:
    assert all([isinstance(price, float) for price in [previous_close_price, close_price]]), "Input prices must be of type float."
    return (close_price/previous_close_price)-1.00

def get_return_history(
    price_close_history: List[Dict]
) -> List[Dict]:
    assert len(price_close_history) > 0, "Input list cannot be empty."
    
    return_history = []
    for i in range(1, len(price_close_history)):
        previous_close_object = price_close_history[i - 1]
        close_object = price_close_history[i]
        
        return_history.append(
            {
                'start_date_close': previous_close_object['date'],
                'end_date_close': close_object['date'],
                'period_return': get_period_return(previous_close_object['price'], close_object['price'])
            }
        )
        
    return return_history
