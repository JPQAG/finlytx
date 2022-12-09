

def get_daily_return(
    previous_close_price: float,
    close_price: float
) -> float:
    assert all([isinstance(price, float) for price in [previous_close_price, close_price]]), "Input prices must be of type float."
    return (close_price/previous_close_price)-1.00


    

