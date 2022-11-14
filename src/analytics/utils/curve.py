from typing import Dict, List
import numpy as np
import datetime

from src.analytics.utils.regression.ns import NelsonSiegelCurve
from src.analytics.utils.regression.nss import NelsonSiegelSvenssonCurve

from src.analytics.utils.regression.calibrate import calibrate_ns_ols, calibrate_nss_ols
from src.analytics.utils.helper import convert_date_series_to_years


def construct_ns_curve(
    pricing_date: datetime.datetime,
    market_curve: List[Dict]
) -> NelsonSiegelCurve:
    """Constructs a Nelson Siegel curve from the market curve to be interpolated.

    Args:
        pricing_date (datetime.datetime): Date to which we are pricing curve (t=0).
        market_curve (List[Dict]): List of dictionaries containing date and rate.

    Returns:
        NelsonSiegelCurve: NelsonSiegelCurve object.
    """

    time_series = convert_date_series_to_years(market_curve, pricing_date)
    time, rate = convert_curve_dict_list_to_lists(time_series)

    time_array = np.array(time)
    rate_array = np.array(rate)
    
    curve, status = calibrate_ns_ols(
        time_array,
        rate_array,
        tau0=1.0
    )

    assert status.success

    return curve

def construct_nss_curve(
    pricing_date: datetime.datetime,
    market_curve: List[Dict]
) -> NelsonSiegelSvenssonCurve:
    """Constructs a Nelson Siegel Svensson curve from the market curve to be interpolated.

    Args:
        pricing_date (datetime.datetime): Date to which wea re pricing curve (t=0)
        market_curve (List[Dict]): List of dictionaries containing date and rate.

    Returns:
        NelsonSiegelSvenssonCurve: NelsonSiegelSvenssonCurve object.
    """

    time_series = convert_date_series_to_years(market_curve, pricing_date)
    time, rate = convert_curve_dict_list_to_lists(time_series)

    time_array = np.array(time)
    rate_array = np.array(rate)
    
    curve, status = calibrate_nss_ols(
        time_array,
        rate_array,
        tau0 = np.array([2.2, 3.1])
    )

    assert status.success

    return curve

def convert_curve_dict_list_to_lists(
    curve_dict_list: List[Dict]
) -> List[List]:
    """Convert a curve of tenors (date, rate) as a list of dictionaries to a list of lists
        one list for date the next for rate.

    Args:
        curve_dict_list (List[Dict]): Curve tenor list of dictionaries {'tenor', 'rate'}

    Returns:
        List[List]: List of dates, rates
    """
    
    times = [dict['time'] for dict in curve_dict_list]
    rates = [dict['rate'] for dict in curve_dict_list]

    return [times, rates]

def bootstrap_curve(
    base_curve: List[Dict]
) -> List[Dict]:
    """Bootstrapped Curve. Used to create zero curve from market/spot curve.

    base_curve must be have evenly spaced tenors.

    Args:
        base_curve (List[Dict]): List of dictionaries containing tenor and rate as floats.

    Returns:
        List[Dict]: _description_
    """
    assert len(base_curve) != 0, f"Provided curve is empty!"
    assert all(isinstance(tenor, float) for tenor in (obj['tenor'] for obj in base_curve)), f"All curve tenors must be of type float!"

    bootstrapped_curve = []

    for tenor_object in base_curve:
        tenor = tenor_object['tenor']
        rate = tenor_object['rate']
        cashflow_sum = 0.0

        if tenor == base_curve[0]['tenor']:
            bootstrapped_curve.append(base_curve[0])
            continue

        for i in range(0, len(bootstrapped_curve)):
            cashflow_sum += rate / (1 + bootstrapped_curve[i]['rate'])**(bootstrapped_curve[i]['tenor'])
        
        final = 1 + rate

        bootstrapped_rate = (((final) / (1 - (cashflow_sum)))**(1/tenor)) - 1

        bootstrapped_curve.append(
            {
                'tenor': tenor,
                'rate': round(bootstrapped_rate, 4)
            }
        )

    return bootstrapped_curve

def forward_curve(
    market_curve: List[Dict],
    forward_tenor: float
) -> Dict[List]:
    """_summary_

    Simple forward curve. Main use case getting market expectations of rate. e.g. 3M rate.

    Therefore if we want 3M swap rate expectations we want:
        The 3M rate today. 
        3M3M
        6M3M
        9M3M
        etc...

    Args:
        market_curve (List[Dict]): _description_
        forward_tenor (float): The fraction of a year representing the forward tenor to forecast.

    Returns:
        List[Dict]: _description_
    """
    forward_curve = []

    # WRITE TESTS FIRST.
    for k in range(0, len(market_curve), forward_curve):
        if k < (forward_tenor -1):
            continue
        elif (k == forward_tenor - 1):
            forward_curve.append(
                {
                    "settle_tenor": market_curve[k]['tenor'] - (forward_tenor/12),
                    "workout_tenor": market_curve[k]['tenor'],
                    "rate": market_curve[k]['rate']
                }
            )
        else:
            forward_curve.append(
                {
                    "settle_tenor": market_curve[k]['tenor'] - (forward_tenor/12),
                    "workout_tenor": market_curve[k]['tenor'],
                    "rate": 
                    (
                        (
                            (
                                (1 + market_curve['zero_rate'][k]) ** market_curve['tenor'][k]) / (((1 + market_curve['zero_rate'][k - market_curve]) ** market_curve['tenor'][k - market_curve]))) - 1)
                }
            )

    return forward_curve
