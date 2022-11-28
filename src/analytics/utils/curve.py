from typing import Dict, List
import numpy as np
import datetime
from src.analytics.utils.financial import implied_forward_rate
from src.analytics.utils.lookup import (
    TIMESERIES_TIME_PERIODS, 
    FRACTION_OF_YEAR_TO_PERIOD_STRING,
    CURVE_OPTIONS
)

from src.analytics.utils.regression.ns import NelsonSiegelCurve
from src.analytics.utils.regression.nss import NelsonSiegelSvenssonCurve

from src.analytics.utils.regression.calibrate import calibrate_ns_ols, calibrate_nss_ols
from src.analytics.utils.helper import convert_date_series_to_years, get_dict_from_list


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

def ns_curve_output(
    NelsonSiegelCurve: NelsonSiegelCurve,
    tenor_range: list
) -> list[Dict]:
    y = NelsonSiegelCurve
    return [{'tenor': tenor, 'rate': y(tenor)} for tenor in tenor_range]

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

def nss_curve_output(
    NelsonSiegelSvenssonCurve: NelsonSiegelSvenssonCurve,
    tenor_range: list
) -> List[Dict]:
    y = NelsonSiegelSvenssonCurve
    return [{'tenor': tenor, 'rate': y(tenor)} for tenor in tenor_range]

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
) -> List[Dict]:
    """_summary_

    Simple forward curve. Main use case getting market expectations of rate. e.g. 3M rate.

    Expected to always be from previous interpolation constructed curve (therefore uniform).

    Therefore if we want 3M swap rate expectations we want:
        The 3M rate today. 
        3M3M
        6M3M
        9M3M
        etc...

    Args:
        market_curve (List[Dict]): Equal monthly (1/12) spaced tenors starting from 1/12. 
        forward_tenor (float): The fraction of a year representing the forward tenor to forecast (a multiple of 1/12).

    Returns:
        List[Dict]: _description_
    """
    assert market_curve != [], f"Curve input must not be an empty list."
    assert len(market_curve) > 1, f"Curve input must contain more than one object!"
    tenors = [object['tenor'] for object in market_curve]
    rates = [object['rate'] for object in market_curve]
    assert all(isinstance(tenor, float) for tenor in tenors), f"Tenors must be of type float."
    assert all(isinstance(rate, float) for rate in rates), f"Rates must be of type float."
    
    forward_curve = []
    freq = FRACTION_OF_YEAR_TO_PERIOD_STRING[forward_tenor]

    for k in range(0, len(market_curve) - 1):
        # get the settlement object.
        settlement_spot_tenor_object = market_curve[k]
        settlement_tenor = settlement_spot_tenor_object['tenor']
        settlement_rate = settlement_spot_tenor_object['rate']
        # Check if there is a corresponding workout spot-tenor object.
        workout_objects_filter = [
            object for object in market_curve if object.get('tenor')==(settlement_tenor+forward_tenor)
        ]
        workout_object = get_dict_from_list(market_curve, "tenor", settlement_tenor+forward_tenor)
        # If there is then calculate and add to the curve.
        if len(workout_objects_filter) > 0:
            workout_tenor = workout_object['tenor']
            workout_rate = workout_object['rate']
            
            forward_curve.append(
                {
                    "settle_tenor": settlement_tenor,
                    "workout_tenor": workout_tenor,
                    "rate": round(implied_forward_rate(settlement_spot_tenor_object, workout_object, freq), 5)
                }
            )
                
    return forward_curve

def curve_set(
    pricing_date: datetime.datetime,
    market_curve: List[Dict],
    forward_rate_set: List[str],
    curve_type: CURVE_OPTIONS="NS"
) -> Dict:
    curve_set = {}
    
    constructed_curve = None
    interpolated_market_curve = None
    match curve_type:
        case "NS":
            constructed_curve = construct_ns_curve(pricing_date, market_curve)
            interpolated_market_curve = ns_curve_output(
                constructed_curve, 
                np.linspace(0, 30, num=30*12).tolist()
            )
        case "NSS":
            constructed_curve = construct_nss_curve(pricing_date, market_curve)
            interpolated_market_curve = ns_curve_output(
                constructed_curve, 
                np.linspace(0, 30, num=30*12).tolist()
            )
    
    zero_curve = bootstrap_curve(interpolated_market_curve)
    # TODO: this should be a dictionary containing all the requested forward period curves.
    forward_curve = forward_curve()