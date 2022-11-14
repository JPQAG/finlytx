import pandas as pd
from pandas.tseries.offsets import DateOffset

TIMESERIES_TIME_PERIODS = {
    "A": {
        "description": "annual",
        "annual_frequency": 1,
        "pd_frequency": DateOffset(years=1)
    },
    "SA": {
        "description": "semi-annual",
        "annual_frequency": 2,
        "pd_frequency": DateOffset(months=6)
    },
    "Q": {
        "description": "quarterly",
        "annual_frequency": 4,
        "pd_frequency": DateOffset(months=3)
    },
    "M": {
        "description": "monthly",
        "annual_frequency": 12,
        "pd_frequency": DateOffset(months=1)
    }
}