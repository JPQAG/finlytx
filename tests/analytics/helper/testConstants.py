import datetime

# Test Cashflow Array
# Array of objects
# Use dates to be specific
# 2022 CFA Program Curriculum Level 1 Page 28
MOCK_SECURITY_CASHFLOW_ARRAY = [
    {
        "date": datetime.datetime(2001, 1, 1),
        "cashflow_value": 1000
    },
    {
        "date": datetime.datetime(2002, 1, 1),
        "cashflow_value": 2000
    },
    {
        "date": datetime.datetime(2003, 1, 1),
        "cashflow_value": 4000
    },
    {
        "date": datetime.datetime(2004, 1, 1),
        "cashflow_value": 5000
    },
    {
        "date": datetime.datetime(2005, 1, 1),
        "cashflow_value": 6000
    },
]

MOCK_SECURITY_FIXED_RATE_CASHFLOW_ARRAY = [
    {
        "date": datetime.datetime(2001, 1, 1),
        "cashflow_value": 10.00
    },
    {
        "date": datetime.datetime(2002, 1, 1),
        "cashflow_value": 10.00
    },
    {
        "date": datetime.datetime(2003, 1, 1),
        "cashflow_value": 10.00
    },
    {
        "date": datetime.datetime(2004, 1, 1),
        "cashflow_value": 10.00
    },
    {
        "date": datetime.datetime(2005, 1, 1),
        "cashflow_value": 10.00
    },
    {
        "date": datetime.datetime(2005, 1, 1),
        "cashflow_value": 100.00
    }
]

MOCK_DISCOUNT_CURVE = [
    {
        "date": datetime.datetime(2001, 1, 1),
        "discount_rate": 0.05
    },
    {
        "date": datetime.datetime(2002, 1, 1),
        "discount_rate": 0.05
    },
    {
        "date": datetime.datetime(2003, 1, 1),
        "discount_rate": 0.05
    },
    {
        "date": datetime.datetime(2004, 1, 1),
        "discount_rate": 0.05
    },
    {
        "date": datetime.datetime(2005, 1, 1),
        "discount_rate": 0.05
    }
]

MOCK_CASHFLOW_AND_DISCOUNT_CURVE = [
    {
        "date": datetime.datetime(2001, 1, 1),
        "cashflow_value": 1000,
        "discount_rate": 0.05
    },
    {
        "date": datetime.datetime(2002, 1, 1),
        "cashflow_value": 2000,
        "discount_rate": 0.05
    },
    {
        "date": datetime.datetime(2003, 1, 1),
        "cashflow_value": 4000,
        "discount_rate": 0.05
    },
    {
        "date": datetime.datetime(2004, 1, 1),
        "cashflow_value": 5000,
        "discount_rate": 0.05
    },
    {
        "date": datetime.datetime(2005, 1, 1),
        "cashflow_value": 6000,
        "discount_rate": 0.05
    },
]

MOCK_BENCHMARK_CURVE = [
    {
        "date": datetime.datetime(2001, 1, 1),
        "rate": 0.01
    },
    {
        "date": datetime.datetime(2002, 1, 1),
        "rate": 0.02
    },
    {
        "date": datetime.datetime(2003, 1, 1),
        "rate": 0.03
    },
    {
        "date": datetime.datetime(2004, 1, 1),
        "rate": 0.035
    },
    {
        "date": datetime.datetime(2005, 1, 1),
        "rate": 0.0375
    }
]

MOCK_BENCHMARK_CURVE_AS_LISTS = [
    [
        datetime.datetime(2001, 1, 1),
        datetime.datetime(2002, 1, 1),
        datetime.datetime(2003, 1, 1),
        datetime.datetime(2004, 1, 1),
        datetime.datetime(2005, 1, 1)
    ],
    [
        0.01,
        0.02,
        0.03,
        0.035,
        0.0375
    ]
]

MOCK_BENCHMARK_CURVE_AS_YEARS = [
    {
        "time": 2.0,
        "rate": 0.01
    },
    {
        "time": 3.0,
        "rate": 0.02
    },
    {
        "time": 4.0,
        "rate": 0.03
    },
    {
        "time": 5.0,
        "rate": 0.035
    },
    {
        "time": 6.0,
        "rate": 0.0375
    }
]

MOCK_BENCHMARK_CURVE_CLEAN_TENOR = [{'tenor': 0.0, 'rate': -0.03}, {'tenor': 2.5, 'rate': 0.02}, {'tenor': 5.0, 'rate': 0.03}, {'tenor': 7.5, 'rate': 0.04}, {'tenor': 10.0, 'rate': 0.05}]

MOCK_BENCHMARK_CURVE_AS_YEARS_AS_LISTS = [
    [
        2.0,
        3.0,
        4.0,
        5.0,
        6.0
    ],
    [
        0.01,
        0.02,
        0.03,
        0.035,
        0.0375
    ]
]

MOCK_SECURITY_PRICING_SERIES = [
    {
        "date": datetime.datetime(2000,1,1),
        "close_price": 100.00
    },
    {
        "date": datetime.datetime(2000,1,2),
        "close_price": 101.00
    },
    {
        "date": datetime.datetime(2000,1,3),
        "close_price":100.00
    },
    {
        "date": datetime.datetime(2000,1,4),
        "close_price": 102.00
    }
]

MOCK_SECURITY_RETURNS = [
    {
        "date": datetime.datetime(2000,1,2),
        "return": 0.01
    },
    {
        "date": datetime.datetime(2000,1,3),
        "return": -0.00990099
    },
    {
        "date": datetime.datetime(2000,1,4),
        "return": 0.02
    }
]

