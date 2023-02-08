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

MOCK_NSS_CURVE_PARAMETERS = [
    2.142562216, 
    -2.649562216,
    19.9532384206, 
    -24.0677865973,
    1.6568604918, 
    1.8145254889
]

MOCK_NSS_CURVE_RESULT = [
    -0.410613, -0.366505, -0.290997, -0.174151,
    -0.028807, 0.129236, 0.287602, 0.438365,
    0.577291, 0.702713, 0.814554, 0.913619,
    1.001124, 1.078417, 1.146814, 1.207524,
    1.261617, 1.310018, 1.353515, 1.392777,
    1.428369, 1.460766, 1.490370, 1.517522,
    1.542510, 1.565581, 1.586946, 1.606787,
    1.625260, 1.642502
]

MOCK_TRADES_INDEX = [
    {
        "trade_date": "2000-01-01",
        "settlement_date": "2000-01-03",
        "isin": "XS12345678901",
        "original_face_value": 100.00,
        "current_face_value": 100.00,
        "side": "B",
        "volume": 100000,
        "price": 101.50
    },
    {
        "trade_date": "2000-02-01",
        "settlement_date": "2000-02-03",
        "isin": "XS12345678902",
        "original_face_value": 100.00,
        "current_face_value": 100.00,
        "side": "B",
        "volume": 100000,
        "price": 100.50
    },
    {
        "trade_date": "2000-03-31",
        "settlement_date": "2000-04-02",
        "isin": "XS12345678902",
        "original_face_value": 100.00,
        "current_face_value": 100.00,
        "side": "S",
        "volume": 50000,
        "price": 101.50
    },
    {
        "trade_date": "2000-03-31",
        "settlement_date": "2000-04-02",
        "isin": "XS12345678902",
        "original_face_value": 100.00,
        "current_face_value": 100.00,
        "side": "S",
        "volume": 50000,
        "price": 101.50
    },
    {
        "trade_date": "2000-06-30",
        "settlement_date": "2000-07-02",
        "isin": "XS12345678901",
        "original_face_value": 100.00,
        "current_face_value": 100.00,
        "side": "S",
        "volume": 50000,
        "price": 100.50
    }
]
