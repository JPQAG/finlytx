import pandas as pd

TIMESERIES_TIME_PERIODS = {
    "A": {
        "description": "annual",
        "pd_frequency": pd.offset(years=1)
    },
    "SA": {
        "description": "semi-annual",
        "pd_frequency": pd.offset(months=6)
    },
    "Q": {
        "description": "quarterly",
        "pd_frequency": pd.offset(months=3)
    },
    "M": {
        "description": "monthly",
        "pd_frequency": pd.offset(months=1)
    }
}