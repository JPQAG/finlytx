import unittest
import datetime
import json

from ..helper.test_utils import (
    test_raises
)

from src.analytics.utils.date_time import (
    _default_date
)

from src.analytics.portfolio.portfolio_performance import (
    get_portfolio_performance_index,
    get_portfolio_performance,
    get_portfolio_valuation_difference
)

class PortfolioPerformanceIndexTestCase(unittest.TestCase):
    
    def test_incorrect_input_type(self):
        
        pricing_date = datetime.datetime(2000,1,1)
        trades = [{},{},{}]
        holdings = { "holdings": "not_empty" }
        cashflows = { "cashflows": "not_empty" }
        prices = { "prices": "not_empty" }
        
        test_cases = [
            ["2000-01-01", trades, holdings, cashflows, prices, f'pricing_date input must be of type datetime.datetime.'],
            [pricing_date, "trades", holdings, cashflows, prices, f'trades input must be of type list.'],
            [pricing_date, trades, "holdings", cashflows, prices, f'holdings input must be of type dict.'],
            [pricing_date, trades, holdings, "cashflows", prices, f'cashflows input must be of type dict.'],
            [pricing_date, trades, holdings, cashflows, "prices", f'prices input must be of type dict.'],
        ]
        
        for test_case in test_cases:
            with self.assertRaises(Exception) as context:
                get_portfolio_performance_index(*test_case[:-1])
            self.assertEqual(context.exception.args[0], test_case[-1])
        
    def test_empty_input(self):
        
        pricing_date = datetime.datetime(2000,1,1)
        trades = [{},{},{}]
        holdings = { "holdings": "not_empty" }
        cashflows = { "cashflows": "not_empty" }
        prices = { "prices": "not_empty" }
        
        test_cases = [
            [pricing_date, [], holdings, cashflows, prices, f'trades input must not be empty.'],
            [pricing_date, trades, {}, cashflows, prices, f'holdings input must not be empty.'],
            [pricing_date, trades, holdings, {}, prices, f'cashflows input must not be empty.'],
            [pricing_date, trades, holdings, cashflows, {}, f'prices input must not be empty.']
        ]
        
        for test_case in test_cases:
            with self.assertRaises(Exception) as context:
                get_portfolio_performance_index(*test_case[:-1])
            self.assertEqual(context.exception.args[0], test_case[-1])
    
    def test_portfolio_performance_index(self):
        pricing_date = datetime.datetime(2001,1,1)
        trades = [
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
                "original_face_value": 100.00,
                "current_face_value": 100.00,
                "isin": "XS12345678902",
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
        cashflows = {
            "XS12345678901" : {
                "2000-02-01": {
                    'date': {
                        "payment_date": "2000-02-01",
                        "record_date": "2000-01-24",
                        "ex_date": "2000-01-23"
                    },
                    'cashflow': {
                        'total': 0.05 / 12 * 100,
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12 * 100,
                            'variable_coupon_interest_component': 0.0,
                            'total_coupon_interest': 0.05 / 12 * 100,
                        },
                        'principal': {
                            'redemption_principal': 0.0,
                            'amortising': 0.0,
                            'total_principal': 0.0
                        }
                    }
                },
                "2000-03-01":{
                    'date': {
                        "payment_date": "2000-03-01",
                        "record_date": "2000-02-22",
                        "ex_date": "2000-02-21"
                    },
                    'cashflow': {
                        'total': 0.05 / 12  * 100,
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12  * 100,
                            'variable_coupon_interest_component': 0.0,
                            'total_coupon_interest': 0.05 / 12  * 100,
                        },
                        'principal': {
                            'redemption_principal': 0.0,
                            'amortising': 0.0,
                            'total_principal': 0.0
                        }
                    }
                }
            },
            "XS12345678902": {
                "2000-02-02": {
                    'date': {
                        "payment_date": "2000-02-02",
                        "record_date": "2000-01-25",
                        "ex_date": "2000-01-24"
                    },
                    'cashflow': {
                        'total': 0.05 / 12  * 100,
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12  * 100,
                            'variable_coupon_interest_component': 0.0,
                            'total_coupon_interest': 0.05 / 12  * 100,
                        },
                        'principal': {
                            'redemption_principal': 0.0,
                            'amortising': 0.0,
                            'total_principal': 0.0
                        }
                    }
                },
                "2000-03-02": {
                    'date': {
                        "payment_date": "2000-03-02",
                        "record_date": "2000-02-25",
                        "ex_date": "2000-02-22"
                    },
                    'cashflow': {
                        'total': 0.05 / 12  * 100,
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12  * 100,
                            'variable_coupon_interest_component': 0.0,
                            'total_coupon_interest': 0.05 / 12  * 100,
                        },
                        'principal': {
                            'redemption_principal': 0.0,
                            'amortising': 0.0,
                            'total_principal': 0.0
                        }
                    }
                },
                "2001-03-02": {
                    'date': {
                        "payment_date": "2001-03-02",
                        "record_date": "2001-02-25",
                        "ex_date": "2001-02-24"
                    },
                    'cashflow': {
                        'total': 0.05 / 12  * 100,
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12  * 100,
                            'variable_coupon_interest_component': 0.0,
                            'total_coupon_interest': 0.05 / 12  * 100,
                        },
                        'principal': {
                            'redemption_principal': 0.0,
                            'amortising': 0.0,
                            'total_principal': 0.0
                        }
                    }
                }
            }
        }
        holdings = {
            "2000-01-03" : {
                "date": "2000-01-03",
                "holdings": {
                    "XS12345678901": {
                        "volume": 100000
                    }
                }
            },
            "2000-02-03" : {
                "date": "2000-02-03",
                "holdings": {
                    "XS12345678901": {
                        "volume": 100000
                    },
                    "XS12345678902": {
                        "volume": 100000
                    }
                }
            },
            "2000-04-02" : {
                "date": "2000-04-02",
                "holdings": {
                    "XS12345678901": {
                        "volume": 100000
                    },
                    "XS12345678902": {
                        "volume": 0
                    }
                }
            },
            "2000-07-02" : {
                "date": "2000-07-02",
                "holdings": {
                    "XS12345678901": {
                        "volume": 50000
                    },
                    "XS12345678902": {
                        "volume": 0
                    }
                }
            }
        }
        prices = {
            "XS12345678901": {
                "2000-01-01": {
                    "date": datetime.datetime(2000,1,1),
                    "per_original_face_value": 100,
                    "currency": "AUD",
                    "base_currency_conversion_rate": 1.00,
                    "value": 99.50  
                },
                "2001-01-01": {
                    "date": datetime.datetime(2001,1,1),
                    "per_original_face_value": 100,
                    "currency": "AUD",
                    "base_currency_conversion_rate": 1.00,
                    "value": 101.50
                },
            },
            "XS12345678902": {
                "2000-01-01": {
                    "date": datetime.datetime(2000,1,1),
                    "per_original_face_value": 100,
                    "currency": "USD",
                    "base_currency_conversion_rate": 0.75,
                    "value": 99.50
                },
                "2001-01-01": {
                    "date": datetime.datetime(2001,1,1),
                    "per_original_face_value": 100,
                    "currency": "USD",
                    "base_currency_conversion_rate": 0.75,
                    "value": 101.50
                }
            }
        }
        
        expected = {
            "start_date": "2000-01-03",
            "end_date": "2001-01-01",
            "index": {
                "2000-01-03": {
                    "date": "2000-01-03",
                    "index_values": {
                        "USD": 100,
                        "AUD": 100
                    },
                    "performance_since_last": {
                        "valuation_change": {},
                        "cashflow_income": {},
                        "invested_capital_delta": {}
                    }
                },
                "2000-02-03": {
                    "date": "2000-02-03",
                    "index_values": {
                        "USD": 99.00497512437812,
                        "AUD": 100.41876046901173
                    },
                    "performance_since_last": {
                        "valuation_change": {
                            "USD": 99500.0,
                            "AUD": 0.0
                        },
                        "cashflow_income": {
                            "USD": 0,
                            "AUD": 416.6666666666667
                        },
                        "invested_capital_delta": {
                            "USD": 100500.0,
                            "AUD": 0
                        }
                    }
                },
                "2000-04-02": {
                    "date": "2000-04-02",
                    "index_values": {
                        "USD": 101.4096185737977,
                        "AUD": 100.83927454132753
                    },
                    "performance_since_last": {
                        "valuation_change": {
                            "USD": -99500.0,
                            "AUD": 0.0
                        },
                        "cashflow_income": {
                            "USD": 416.6666666666667,
                            "AUD": 416.6666666666667
                        },
                        "invested_capital_delta": {
                            "USD": -101500.0,
                            "AUD": 0
                        }
                    }
                },
                "2000-07-02": {
                    "date": "2000-07-02",
                    "index_values": {
                        "USD": 101.4096185737977,
                        "AUD": 101.34600456414826
                    },
                    "performance_since_last": {
                        "valuation_change": {
                            "USD": 0.0,
                            "AUD": -49750.0
                        },
                        "cashflow_income": {
                            "USD": 0,
                            "AUD": 0
                        },
                        "invested_capital_delta": {
                            "USD": 0,
                            "AUD": -50250.0
                        }
                    }
                }
            }
        }

        result = get_portfolio_performance_index(
            pricing_date,
            trades,
            holdings,
            cashflows,
            prices,
        )
        
        with open("result.json", "w") as f:
            f.write(json.dumps(result, indent=4))
        
        self.assertEqual(result, expected)

class PortfolioPerformanceTestCase(unittest.TestCase):
    
    def test_incorrect_input_type(self):
        
        pricing_date = datetime.datetime(2001,1,1)
        start_valuation = {
            "total_valuation": {},
            "position_valuation": {}
        }
        end_valuation = {
            "total_valuation": {
                "AUD": 101500,
                "USD": 101500
            },
            "position_valuation": {
                "XS1234567890": {
                    "currency": "AUD",
                    "volume": 100000,
                    "price": {
                        "date": datetime.datetime(2000,1,1),
                        "per_original_face_value": 100,
                        "currency": "AUD",
                        "base_currency_conversion_rate": 1.00,
                        "value": 101.50
                    },
                    "valuation": 101500.00
                },
                "XS1234567891": {
                    "currency": "USD",
                    "volume": 100000,
                    "price": {
                        "date": datetime.datetime(2000,1,1),
                        "per_original_face_value": 100,
                        "currency": "USD",
                        "base_currency_conversion_rate": 0.75,
                        "value": 101.50
                    },
                    "valuation": 101500.00
                }
            }
        }
        cashflows = {
            "2000-02-01": {
                "XS12345678901" : {
                    'date': {
                        "payment_date": "2000-02-01",
                        "record_date": "2000-01-24",
                        "ex_date": "2000-01-23"
                    },
                    'cashflow': {
                        'total': 0.05 / 12 * 100000,
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12 * 100000,
                            'variable_coupon_interest_component': 0 * 100000,
                            'total_coupon_interest': 0.05 / 12 * 100000,
                        },
                        'principal': {
                            'redemption_principal': 0 * 100000,
                            'amortising': 0 * 100000,
                            'total_principal': 0 * 100000
                        }
                    }
                }
            },
            "2000-03-01": {
                "XS12345678901": {
                    'date': {
                        "payment_date": "2000-03-01",
                        "record_date": "2000-02-22",
                        "ex_date": "2000-02-21"
                    },
                    'cashflow': {
                        'total': 0.05 / 12  *100000,
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12  * 100000,
                            'variable_coupon_interest_component': 0 * 100000,
                            'total_coupon_interest': 0.05 / 12  * 100000,
                        },
                        'principal': {
                            'redemption_principal': 0 * 100000,
                            'amortising': 0 * 100000,
                            'total_principal': 0 * 100000
                        }
                    }
                }
            },
            "2000-03-02": {
                "XS12345678902": {
                    'date': {
                        "payment_date": "2000-03-02",
                        "record_date": "2000-02-25",
                        "ex_date": "2000-02-22"
                    },
                    'cashflow': {
                        'total': 0.05 / 12  * 100000,
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12  * 100000,
                            'variable_coupon_interest_component': 0 * 100000,
                            'total_coupon_interest': 0.05 / 12  * 100000,
                        },
                        'principal': {
                            'redemption_principal': 0 * 100000,
                            'amortising': 0 * 100000,
                            'total_principal': 0 * 100000
                        }
                    }
                }   
            }
        }
        holdings = {
            "2000-01-03" : {
                "date": "2000-01-03",
                "holdings": {
                    "XS12345678901": {
                        "volume": 100000
                    }
                }
            },
            "2000-02-03" : {
                "date": "2000-02-03",
                "holdings": {
                    "XS12345678901": {
                        "volume": 100000
                    },
                    "XS12345678902": {
                        "volume": 100000
                    }
                }
            }
        }
        prices = {
            "XS1234567890": {
                "2000-01-01": {
                    "date": datetime.datetime(2000,1,1),
                    "per_original_face_value": 100,
                    "currency": "AUD",
                    "base_currency_conversion_rate": 1.00,
                    "value": 99.50
                },
                "2001-01-01": {
                    "date": datetime.datetime(2001,1,1),
                    "per_original_face_value": 100,
                    "currency": "AUD",
                    "base_currency_conversion_rate": 1.00,
                    "value": 101.50
                },
            },
            "XS1234567891": {
                "2000-01-01": {
                    "date": datetime.datetime(2000,1,1),
                    "per_original_face_value": 100,
                    "currency": "USD",
                    "base_currency_conversion_rate": 0.75,
                    "value": 99.50
                },
                "2001-01-01": {
                    "date": datetime.datetime(2001,1,1),
                    "per_original_face_value": 100,
                    "currency": "USD",
                    "base_currency_conversion_rate": 0.75,
                    "value": 101.50
                }
            }
        }
        
        test_cases = [
            ["2000-01-01", start_valuation, end_valuation, prices, cashflows, holdings, 'pricing_date input must be of type datetime.datetime.'],
            [pricing_date, "start_valuation", end_valuation, prices, cashflows, holdings, 'start_valuation input must be of type dict.'],
            [pricing_date, start_valuation, "end_valuation", prices, cashflows, holdings, 'end_valuation input must be of type dict.'],
            [pricing_date, start_valuation, end_valuation, "prices", cashflows, holdings, 'prices input must be of type dict.'],
            [pricing_date, start_valuation, end_valuation, prices, "cashflows", holdings, 'cashflows input must be of type dict.'],
            [pricing_date, start_valuation, end_valuation, prices, cashflows, "holdings", 'holdings input must be of type dict.']
        ]
        
        for test_case in test_cases:
            with self.assertRaises(Exception) as context:
                get_portfolio_performance(*test_case[:-1])
            self.assertEqual(context.exception.args[0], test_case[-1])
        
        
    def test_empty_input(self):
        
        pricing_date = datetime.datetime(2001,1,1)
        start_valuation = {
            "total_valuation": {},
            "position_valuation": {}
        }
        end_valuation = {
            "total_valuation": {
                "AUD": 101500,
                "USD": 101500
            },
            "position_valuation": {
                "XS1234567890": {
                    "currency": "AUD",
                    "volume": 100000,
                    "price": {
                        "date": datetime.datetime(2000,1,1),
                        "per_original_face_value": 100,
                        "currency": "AUD",
                        "base_currency_conversion_rate": 1.00,
                        "value": 101.50
                    },
                    "valuation": 101500.00
                },
                "XS1234567891": {
                    "currency": "USD",
                    "volume": 100000,
                    "price": {
                        "date": datetime.datetime(2000,1,1),
                        "per_original_face_value": 100,
                        "currency": "USD",
                        "base_currency_conversion_rate": 0.75,
                        "value": 101.50
                    },
                    "valuation": 101500.00
                }
            }
        }
        cashflows = {
            "2000-02-01": {
                "XS12345678901" : {
                    'date': {
                        "payment_date": "2000-02-01",
                        "record_date": "2000-01-24",
                        "ex_date": "2000-01-23"
                    },
                    'cashflow': {
                        'total': 0.05 / 12 * 100000,
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12 * 100000,
                            'variable_coupon_interest_component': 0 * 100000,
                            'total_coupon_interest': 0.05 / 12 * 100000,
                        },
                        'principal': {
                            'redemption_principal': 0 * 100000,
                            'amortising': 0 * 100000,
                            'total_principal': 0 * 100000
                        }
                    }
                }
            },
            "2000-03-01": {
                "XS12345678901": {
                    'date': {
                        "payment_date": "2000-03-01",
                        "record_date": "2000-02-22",
                        "ex_date": "2000-02-21"
                    },
                    'cashflow': {
                        'total': 0.05 / 12  *100000,
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12  * 100000,
                            'variable_coupon_interest_component': 0 * 100000,
                            'total_coupon_interest': 0.05 / 12  * 100000,
                        },
                        'principal': {
                            'redemption_principal': 0 * 100000,
                            'amortising': 0 * 100000,
                            'total_principal': 0 * 100000
                        }
                    }
                }
            },
            "2000-03-02": {
                "XS12345678902": {
                    'date': {
                        "payment_date": "2000-03-02",
                        "record_date": "2000-02-25",
                        "ex_date": "2000-02-22"
                    },
                    'cashflow': {
                        'total': 0.05 / 12  * 100000,
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12  * 100000,
                            'variable_coupon_interest_component': 0 * 100000,
                            'total_coupon_interest': 0.05 / 12  * 100000,
                        },
                        'principal': {
                            'redemption_principal': 0 * 100000,
                            'amortising': 0 * 100000,
                            'total_principal': 0 * 100000
                        }
                    }
                }   
            }
        }
        holdings = {
            "2000-01-03" : {
                "date": "2000-01-03",
                "holdings": {
                    "XS12345678901": {
                        "volume": 100000
                    }
                }
            },
            "2000-02-03" : {
                "date": "2000-02-03",
                "holdings": {
                    "XS12345678901": {
                        "volume": 100000
                    },
                    "XS12345678902": {
                        "volume": 100000
                    }
                }
            }
        }
        prices = {
            "XS1234567890": {
                "2000-01-01": {
                    "date": datetime.datetime(2000,1,1),
                    "per_original_face_value": 100,
                    "currency": "AUD",
                    "base_currency_conversion_rate": 1.00,
                    "value": 99.50
                },
                "2001-01-01": {
                    "date": datetime.datetime(2001,1,1),
                    "per_original_face_value": 100,
                    "currency": "AUD",
                    "base_currency_conversion_rate": 1.00,
                    "value": 101.50
                },
            },
            "XS1234567891": {
                "2000-01-01": {
                    "date": datetime.datetime(2000,1,1),
                    "per_original_face_value": 100,
                    "currency": "USD",
                    "base_currency_conversion_rate": 0.75,
                    "value": 99.50
                },
                "2001-01-01": {
                    "date": datetime.datetime(2001,1,1),
                    "per_original_face_value": 100,
                    "currency": "USD",
                    "base_currency_conversion_rate": 0.75,
                    "value": 101.50
                }
            }
        }
        
        test_cases = [
            [pricing_date, {}, end_valuation, prices, cashflows, holdings, "start_valuation input must not be empty."],
            [pricing_date, start_valuation, {}, prices, cashflows, holdings, "end_valuation input must not be empty."],
            [pricing_date, start_valuation, end_valuation, {}, cashflows, holdings, "prices input must not be empty."],
            [pricing_date, start_valuation, end_valuation, prices, {}, holdings, "cashflows input must not be empty."],
            [pricing_date, start_valuation, end_valuation, prices, cashflows, {}, "holdings input must not be empty."]
        ]
        
        for test_case in test_cases:
            with self.assertRaises(Exception) as context:
                get_portfolio_performance(*test_case[:-1])
            self.assertEqual(context.exception.args[0], test_case[-1])
        

    def test_zero_to_non_zero_valuation_no_cashflow(self):
        
        pricing_date = datetime.datetime(2001,1,1)
        start_valuation = {
            "date": datetime.datetime(2000,1,1),
            "valuation": {
                "total_valuation": {},
                "position_valuation": {}
            }            
        }
        end_valuation = {
            "date": datetime.datetime(2001,1,1),
            "valuation": {
                "total_valuation": {
                    "AUD": 101500,
                    "USD": 101500
                },
                "position_valuation": {
                    "XS1234567890": {
                        "currency": "AUD",
                        "volume": 100000,
                        "price": {
                            "date": datetime.datetime(2000,1,1),
                            "per_original_face_value": 100,
                            "currency": "AUD",
                            "base_currency_conversion_rate": 1.00,
                            "value": 101.50
                        },
                        "valuation": 101500.00
                    },
                    "XS1234567891": {
                        "currency": "USD",
                        "volume": 100000,
                        "price": {
                            "date": datetime.datetime(2000,1,1),
                            "per_original_face_value": 100,
                            "currency": "USD",
                            "base_currency_conversion_rate": 0.75,
                            "value": 101.50
                        },
                        "valuation": 101500.00
                    }
                }
            }
            
        }
        cashflows = {
            "XS12345678901" : {
                "2000-02-01": {
                    'date': {
                        "payment_date": "2000-02-01",
                        "record_date": "2000-01-24",
                        "ex_date": "2000-01-23"
                    },
                    'cashflow': {
                        'total': 0.05 / 12 * 100,
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12 * 100,
                            'variable_coupon_interest_component': 0.0,
                            'total_coupon_interest': 0.05 / 12 * 100,
                        },
                        'principal': {
                            'redemption_principal': 0.0,
                            'amortising': 0.0,
                            'total_principal': 0.0
                        }
                    }
                },
                "2000-03-01":{
                    'date': {
                        "payment_date": "2000-03-01",
                        "record_date": "2000-02-22",
                        "ex_date": "2000-02-21"
                    },
                    'cashflow': {
                        'total': 0.05 / 12  * 100,
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12  * 100,
                            'variable_coupon_interest_component': 0.0,
                            'total_coupon_interest': 0.05 / 12  * 100,
                        },
                        'principal': {
                            'redemption_principal': 0.0,
                            'amortising': 0.0,
                            'total_principal': 0.0
                        }
                    }
                }
            },
            "XS12345678902": {
                "2000-02-02": {
                    'date': {
                        "payment_date": "2000-02-02",
                        "record_date": "2000-01-25",
                        "ex_date": "2000-01-24"
                    },
                    'cashflow': {
                        'total': 0.05 / 12  * 100,
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12  * 100,
                            'variable_coupon_interest_component': 0.0,
                            'total_coupon_interest': 0.05 / 12  * 100,
                        },
                        'principal': {
                            'redemption_principal': 0.0,
                            'amortising': 0.0,
                            'total_principal': 0.0
                        }
                    }
                },
                "2000-03-02": {
                    'date': {
                        "payment_date": "2000-03-02",
                        "record_date": "2000-02-25",
                        "ex_date": "2000-02-22"
                    },
                    'cashflow': {
                        'total': 0.05 / 12  * 100,
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12  * 100,
                            'variable_coupon_interest_component': 0.0,
                            'total_coupon_interest': 0.05 / 12  * 100,
                        },
                        'principal': {
                            'redemption_principal': 0.0,
                            'amortising': 0.0,
                            'total_principal': 0.0
                        }
                    }
                },
                "2001-03-02": {
                    'date': {
                        "payment_date": "2001-03-02",
                        "record_date": "2001-02-25",
                        "ex_date": "2001-02-24"
                    },
                    'cashflow': {
                        'total': 0.05 / 12  * 100,
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12  * 100,
                            'variable_coupon_interest_component': 0.0,
                            'total_coupon_interest': 0.05 / 12  * 100,
                        },
                        'principal': {
                            'redemption_principal': 0.0,
                            'amortising': 0.0,
                            'total_principal': 0.0
                        }
                    }
                }
            }
        }
        holdings = {
            "2000-01-03" : {
                "date": "2000-01-03",
                "holdings": {
                    "XS12345678901": {
                        "volume": 100000
                    }
                }
            },
            "2000-02-03" : {
                "date": "2000-02-03",
                "holdings": {
                    "XS12345678901": {
                        "volume": 100000
                    },
                    "XS12345678902": {
                        "volume": 100000
                    }
                }
            },
            "2000-04-02" : {
                "date": "2000-04-02",
                "holdings": {
                    "XS12345678901": {
                        "volume": 100000
                    },
                    "XS12345678902": {
                        "volume": 0
                    }
                }
            },
            "2000-07-02" : {
                "date": "2000-07-02",
                "holdings": {
                    "XS12345678901": {
                        "volume": 50000
                    },
                    "XS12345678902": {
                        "volume": 0
                    }
                }
            }
        }
        prices = {
            "XS1234567890": {
                "2000-01-01": {
                    "date": datetime.datetime(2000,1,1),
                    "per_original_face_value": 100,
                    "currency": "AUD",
                    "base_currency_conversion_rate": 1.00,
                    "value": 99.50
                },
                "2001-01-01": {
                    "date": datetime.datetime(2001,1,1),
                    "per_original_face_value": 100,
                    "currency": "AUD",
                    "base_currency_conversion_rate": 1.00,
                    "value": 101.50
                },
            },
            "XS1234567891": {
                "2000-01-01": {
                    "date": datetime.datetime(2000,1,1),
                    "per_original_face_value": 100,
                    "currency": "USD",
                    "base_currency_conversion_rate": 0.75,
                    "value": 99.50
                },
                "2001-01-01": {
                    "date": datetime.datetime(2001,1,1),
                    "per_original_face_value": 100,
                    "currency": "USD",
                    "base_currency_conversion_rate": 0.75,
                    "value": 101.50
                }
            }
        }
        
        expected = {
            "pricing_date": "2001-01-01",
            "start_date": "2000-01-01",
            "end_date": "2001-01-01",
            "investment_value_change": {
                "valuation_change" : {
                    "AUD": 101500,
                    "USD": 101500    
                },
                "cashflow_income": {
                    "2000-02-01": {
                        "XS12345678901" : {
                            'date': {
                                "payment_date": "2000-02-01",
                                "record_date": "2000-01-24",
                                "ex_date": "2000-01-23"
                            },
                            'cashflow': {
                                'total': 0.05 / 12 * 100000,
                                'coupon_interest': {
                                    'fixed_coupon_interest_component': 0.05 / 12 * 100000,
                                    'variable_coupon_interest_component': 0 * 100000,
                                    'total_coupon_interest': 0.05 / 12 * 100000,
                                },
                                'principal': {
                                    'redemption_principal': 0 * 100000,
                                    'amortising': 0 * 100000,
                                    'total_principal': 0 * 100000
                                }
                            }
                        }
                    },
                    "2000-03-01": {
                        "XS12345678901": {
                            'date': {
                                "payment_date": "2000-03-01",
                                "record_date": "2000-02-22",
                                "ex_date": "2000-02-21"
                            },
                            'cashflow': {
                                'total': 0.05 / 12  *100000,
                                'coupon_interest': {
                                    'fixed_coupon_interest_component': 0.05 / 12  * 100000,
                                    'variable_coupon_interest_component': 0 * 100000,
                                    'total_coupon_interest': 0.05 / 12  * 100000,
                                },
                                'principal': {
                                    'redemption_principal': 0 * 100000,
                                    'amortising': 0 * 100000,
                                    'total_principal': 0 * 100000
                                }
                            }
                        }
                    },
                    "2000-03-02": {
                        "XS12345678902": {
                            'date': {
                                "payment_date": "2000-03-02",
                                "record_date": "2000-02-25",
                                "ex_date": "2000-02-22"
                            },
                            'cashflow': {
                                'total': 0.05 / 12  * 100000,
                                'coupon_interest': {
                                    'fixed_coupon_interest_component': 0.05 / 12  * 100000,
                                    'variable_coupon_interest_component': 0 * 100000,
                                    'total_coupon_interest': 0.05 / 12  * 100000,
                                },
                                'principal': {
                                    'redemption_principal': 0 * 100000,
                                    'amortising': 0 * 100000,
                                    'total_principal': 0 * 100000
                                }
                            }
                        }   
                    }
                }
            }
        }
        
        result = get_portfolio_performance(pricing_date, start_valuation, end_valuation, prices, cashflows, holdings)
        
        self.assertEqual(result, expected)

class GetPortfolioValuationDifferenceTestCase(unittest.TestCase):
    
    def test_zero_to_non_zero(self):
        start_valuation = {
            "date": datetime.datetime(2000,1,1),
            "valuation": {
                "total_valuation": {},
                "position_valuation": {}
            }            
        }
        end_valuation = {
            "date": "2001-01-01",
            "valuation": {
                "total_valuation": {
                    "AUD": 101500,
                    "USD": 101500
                },
                "position_valuation": {
                    "XS1234567890": {
                        "currency": "AUD",
                        "volume": 100000,
                        "price": {
                            "date": datetime.datetime(2000,1,1),
                            "per_original_face_value": 100,
                            "currency": "AUD",
                            "base_currency_conversion_rate": 1.00,
                            "value": 101.50
                        },
                        "valuation": 101500.00
                    },
                    "XS1234567891": {
                        "currency": "USD",
                        "volume": 100000,
                        "price": {
                            "date": datetime.datetime(2000,1,1),
                            "per_original_face_value": 100,
                            "currency": "USD",
                            "base_currency_conversion_rate": 0.75,
                            "value": 101.50
                        },
                        "valuation": 101500.00
                    }
                }
            }
        }
        expected = {
            "valuation_change": {
                "AUD": 101500,
                "USD": 101500
            }
        }
        
        result = get_portfolio_valuation_difference(start_valuation, end_valuation)
        
        self.assertEqual(result, expected)
        
    def test_no_change(self):
        start_valuation = {
            "date": "2000-01-01",
            "valuation": {
                "total_valuation": {
                    "AUD": 101500,
                    "USD": 101500
                },
                "position_valuation": {
                    "XS1234567890": {
                        "currency": "AUD",
                        "volume": 100000,
                        "price": {
                            "date": datetime.datetime(2000,1,1),
                            "per_original_face_value": 100,
                            "currency": "AUD",
                            "base_currency_conversion_rate": 1.00,
                            "value": 101.50
                        },
                        "valuation": 101500.00
                    },
                    "XS1234567891": {
                        "currency": "USD",
                        "volume": 100000,
                        "price": {
                            "date": datetime.datetime(2000,1,1),
                            "per_original_face_value": 100,
                            "currency": "USD",
                            "base_currency_conversion_rate": 0.75,
                            "value": 101.50
                        },
                        "valuation": 101500.00
                    }
                }
            }
        }
        
        end_valuation = {
            "date": "2001-01-01",
            "valuation": {
                "total_valuation": {
                    "AUD": 101500,
                    "USD": 101500
                },
                "position_valuation": {
                    "XS1234567890": {
                        "currency": "AUD",
                        "volume": 100000,
                        "price": {
                            "date": datetime.datetime(2001,1,1),
                            "per_original_face_value": 100,
                            "currency": "AUD",
                            "base_currency_conversion_rate": 1.00,
                            "value": 101.50
                        },
                        "valuation": 101500.00
                    },
                    "XS1234567891": {
                        "currency": "USD",
                        "volume": 100000,
                        "price": {
                            "date": datetime.datetime(2001,1,1),
                            "per_original_face_value": 100,
                            "currency": "USD",
                            "base_currency_conversion_rate": 0.75,
                            "value": 101.50
                        },
                        "valuation": 101500.00
                    }
                }
            }
        }
        
        expected = {
            "valuation_change": {
                "AUD": 0,
                "USD": 0
            }
        }
        
                
        result = get_portfolio_valuation_difference(start_valuation, end_valuation)
        
        self.assertEqual(result, expected)
        
    def test_negative_change(self):
        start_valuation = {
            "date": "2000-01-01",
            "valuation": {
                "total_valuation": {
                    "AUD": 101500,
                    "USD": 100000
                },
                "position_valuation": {
                    "XS1234567890": {
                        "currency": "AUD",
                        "volume": 100000,
                        "price": {
                            "date": datetime.datetime(2000,1,1),
                            "per_original_face_value": 100,
                            "currency": "AUD",
                            "base_currency_conversion_rate": 1.00,
                            "value": 101.50
                        },
                        "valuation": 101500.00
                    },
                    "XS1234567891": {
                        "currency": "USD",
                        "volume": 100000,
                        "price": {
                            "date": datetime.datetime(2000,1,1),
                            "per_original_face_value": 100,
                            "currency": "USD",
                            "base_currency_conversion_rate": 0.75,
                            "value": 100.50
                        },
                        "valuation": 100000.00
                    }
                }    
            }
        }
        
        end_valuation = {
            "date": "2001-01-01",
            "valuation": {
                "total_valuation": {
                    "AUD": 101500,
                    "USD": 50000
                },
                "position_valuation": {
                    "XS1234567890": {
                        "currency": "AUD",
                        "volume": 100000,
                        "price": {
                            "date": datetime.datetime(2001,1,1),
                            "per_original_face_value": 100,
                            "currency": "AUD",
                            "base_currency_conversion_rate": 1.00,
                            "value": 101.50
                        },
                        "valuation": 101500.00
                    },
                    "XS1234567891": {
                        "currency": "USD",
                        "volume": 50000,
                        "price": {
                            "date": datetime.datetime(2001,1,1),
                            "per_original_face_value": 100,
                            "currency": "USD",
                            "base_currency_conversion_rate": 0.75,
                            "value": 100.00
                        },
                        "valuation": 50000.00
                    }
                }    
            }
        }
        
        expected = {
            "valuation_change": {
                "AUD": 0,
                "USD": -50000
            }
        }
            
        result = get_portfolio_valuation_difference(start_valuation, end_valuation)
        
        self.assertEqual(result, expected)
