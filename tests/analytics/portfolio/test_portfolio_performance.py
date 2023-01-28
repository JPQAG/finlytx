import unittest
import datetime

from ..helper.test_utils import (
    test_raises
)

from src.analytics.portfolio.portfolio_performance import (
    get_portfolio_performance_index,
    get_portfolio_performance
)

class portfolioPerformanceIndexTestCase(unittest.TestCase):
    
    def test_incorrect_input_type(self):
        
        pricing_date = datetime.datetime(2000,1,1)
        holdings = { "holdings": "not_empty" }
        cashflows = { "cashflows": "not_empty" }
        prices = { "prices": "not_empty" }
        
        test_raises(self, get_portfolio_performance_index("2000-01-01", holdings, cashflows, prices), f'pricing_date must be of type datetime.datetime.')
        test_raises(self, get_portfolio_performance_index(pricing_date, "holdings", cashflows, prices), f'holdings must be of type dict.')
        test_raises(self, get_portfolio_performance_index(pricing_date, holdings, "cashflows", prices), f'cashflows must be of type dict.')
        test_raises(self, get_portfolio_performance_index(pricing_date, holdings, cashflows, "prices"), f'prices must be of type dict.')
        
    def test_empty_input(self):
        
        pricing_date = datetime.datetime(2000,1,1)
        holdings = { "holdings": "not_empty" }
        cashflows = { "cashflows": "not_empty" }
        prices = { "prices": "not_empty" }
        
        test_raises(self, get_portfolio_performance_index(pricing_date, {}, cashflows, prices), f'holdings must not be empty.')
        test_raises(self, get_portfolio_performance_index(pricing_date, holdings, {}, prices), f'cashflows must not be empty.')
        test_raises(self, get_portfolio_performance_index(pricing_date, holdings, cashflows, {}), f'prices must not be empty.')
    
    def test_portfolio_performance_index(self):
        pass

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
        
        test_raises(self, get_portfolio_performance("2000-01-01", start_valuation, end_valuation, prices, cashflows, holdings), f'pricing_date must be of type datetime.datetime.')
        test_raises(self, get_portfolio_performance(pricing_date, "start_valuation", end_valuation, prices, cashflows, holdings), f'start_valuation must be of type dict.')
        test_raises(self, get_portfolio_performance(pricing_date, start_valuation, "end_valuation", prices, cashflows, holdings), f'end_valuation must be of type dict.')
        test_raises(self, get_portfolio_performance(pricing_date, start_valuation, end_valuation, "prices", cashflows, holdings), f'prices must be of type dict.')
        test_raises(self, get_portfolio_performance(pricing_date, start_valuation, end_valuation, prices, "cashflows", holdings), f'cashflows must be of type dict.')
        test_raises(self, get_portfolio_performance(pricing_date, start_valuation, end_valuation, prices, cashflows, "holdings"), f'holdings must be of type dict.')
        
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
        
        test_raises(self, get_portfolio_performance(pricing_date, {}, end_valuation, prices, cashflows, holdings), "start_valuation must not be empty.")
        test_raises(self, get_portfolio_performance(pricing_date, start_valuation, {}, prices, cashflows, holdings), "end_valuation must not be empty.")
        test_raises(self, get_portfolio_performance(pricing_date, start_valuation, end_valuation, {}, cashflows, holdings), "prices must not be empty.")
        test_raises(self, get_portfolio_performance(pricing_date, start_valuation, end_valuation, prices, {}, holdings), "cashflows must not be empty.")
        test_raises(self, get_portfolio_performance(pricing_date, start_valuation, end_valuation, prices, cashflows, {}), "holdings must not be empty.")
        
    def test_portfolio_performance(self):
        
        pricing_date = datetime.datetime(2000,1,1)
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
        
        expected = {
            "pricing_date": "2001-01-01",
            "start_date": "2000-01-01",
            "end_date": "2001-01-01",
            "investment_value_change": {
                "valuation" : {
                    "AUD": 101500,
                    "USD": 101500    
                },
                "cashflow": {
                    "AUD": 101500*0.05,
                    "USD": 101500*0.05
                }
            }
        }
        
        result = get_portfolio_performance(pricing_date, start_valuation, end_valuation, prices, cashflows, holdings)
        
        self.assertEqual(result, expected)

