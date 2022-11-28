import pandas as pd
from pandas.tseries.offsets import DateOffset

TIMESERIES_TIME_PERIODS = {
    "A": {
        "description": "annual",
        "annual_frequency": 1,
        "pd_frequency": DateOffset(years=1),
        "fraction_of_year": 1.0
    },
    "SA": {
        "description": "semi-annual",
        "annual_frequency": 2,
        "pd_frequency": DateOffset(months=6),
        "fraction_of_year": 0.50
    },
    "Q": {
        "description": "quarterly",
        "annual_frequency": 4,
        "pd_frequency": DateOffset(months=3),
        "fraction_of_year": 3/12
    },
    "M": {
        "description": "monthly",
        "annual_frequency": 12,
        "pd_frequency": DateOffset(months=1),
        "fraction_of_year": 1/12
    }
}

FRACTION_OF_YEAR_TO_PERIOD_STRING = {
    1/12: "M",
    3/12: "Q",
    6/12: "SA",
    12/12: "A"
}

CURVE_OPTIONS = [
    "NS",
    "NSS"
]
