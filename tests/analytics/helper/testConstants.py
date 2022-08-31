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




