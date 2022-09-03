from typing import Dict, List
import numpy as np
import datetime

from analytics.utils.regression.ns import NelsonSiegelCurve
from analytics.utils.regression.nss import NelsonSiegelSvenssonCurve

from analytics.utils.regression.calibrate import calibrate_ns_ols, calibrate_nss_ols
from analytics.utils.helper import convert_date_series_to_years


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
        curve_dict_list (List[Dict]): Curve tenor list of dictionaries

    Returns:
        List[List]: List of dates, rates
    """
    
    times = [dict['time'] for dict in curve_dict_list]
    rates = [dict['rate'] for dict in curve_dict_list]

    return [times, rates]
