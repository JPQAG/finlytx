import unittest

from finx.analytics.utils.date_time import (
    _default_date
)

from finx.analytics.portfolio.portfolio_cashflows import (
    get_portfolio_future_cashflows,
    get_portfolio_historical_cashflows,
    _get_cashflow_given_holdings
)

class PortfolioFutureCashflowsTest(unittest.TestCase):
    
    def test_get_portfolio_future_cashflows_portfolio_holdings_incorrect_type(self):
        with self.assertRaises(Exception) as context:
            get_portfolio_future_cashflows(
                "Not a Dict",
                {}
            )
        self.assertEqual(context.exception.args[0], "portfolio_holdings input must be of type Dict.")
        
    def test_get_portfolio_future_cashflows_security_cashflows_object_incorrect_type(self):
        with self.assertRaises(Exception) as context:
            get_portfolio_future_cashflows(
                {},
                "Not a Dict"
            )
        self.assertEqual(context.exception.args[0], "security_cashflows_object input must be of type Dict.")
        
    def test_empty_holdings_input(self):
        with self.assertRaises(Exception) as context:
            get_portfolio_future_cashflows(
                {},
                { "Not empty": "Not empty" }
            )
        self.assertEqual(context.exception.args[0], "portfolio_holdings input must not be empty.")
        
    def test_empty_security_cashflows_objects(self):
        with self.assertRaises(Exception) as context:
            get_portfolio_future_cashflows(
                { "Not empty": "Not empty" },
                {}
            )
        self.assertEqual(context.exception.args[0], "security_cashflows_object input must not be empty.")

    def test_get_portfolio_future_cashflows(self):
        
        portfolio_holdings = {
            "date": "2000-01-01",
            "holdings": {
                "XS12345678901": {
                    "volume": 100000.0
                },
                "XS12345678902": {
                    "volume": 100000.0
                }
            }
        }
                
        security_lifetime_cashflow_object = {
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
                }   
            }
        }
    
        expected_result = {
            "2000-02-01": {
                "XS12345678901" : {
                    'date': {
                        "payment_date": "2000-02-01",
                        "record_date": "2000-01-24",
                        "ex_date": "2000-01-23"
                    },
                    'cashflow': {
                        'total': 0.05 / 12 * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12 * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                            'variable_coupon_interest_component': 0 * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                            'total_coupon_interest': 0.05 / 12 * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                        },
                        'principal': {
                            'redemption_principal': 0 * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                            'amortising': 0 * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                            'total_principal': 0 * portfolio_holdings["holdings"]["XS12345678901"]["volume"]
                        }
                    }
                }
            },
            "2000-02-02": {
                "XS12345678902": {
                    'date': {
                        "payment_date": "2000-02-02",
                        "record_date": "2000-01-25",
                        "ex_date": "2000-01-24"
                    },
                    'cashflow': {
                        'total': 0.05 / 12 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                            'variable_coupon_interest_component': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                            'total_coupon_interest': 0.05 / 12 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                        },
                        'principal': {
                            'redemption_principal': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                            'amortising': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                            'total_principal': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"]
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
                        'total': 0.05 / 12  * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12  * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                            'variable_coupon_interest_component': 0 * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                            'total_coupon_interest': 0.05 / 12  * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                        },
                        'principal': {
                            'redemption_principal': 0 * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                            'amortising': 0 * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                            'total_principal': 0 * portfolio_holdings["holdings"]["XS12345678901"]["volume"]
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
                        'total': 0.05 / 12  * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12  * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                            'variable_coupon_interest_component': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                            'total_coupon_interest': 0.05 / 12  * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                        },
                        'principal': {
                            'redemption_principal': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                            'amortising': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                            'total_principal': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"]
                        }
                    }
                }   
            }
        }
    
        result = get_portfolio_future_cashflows(portfolio_holdings, security_lifetime_cashflow_object)
    
        self.assertDictEqual(result, expected_result)
        
    def test_get_portfolio_future_cashflows_in_ex_date(self):
            
        portfolio_holdings = {
            "date": "2000-01-24",
            "holdings": {
                "XS12345678901": {
                    "volume": 100000.0
                },
                "XS12345678902": {
                    "volume": 100000.0
                }
            }
        }
                
        security_lifetime_cashflow_object = {
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
                }   
            }
        }
    
        expected_result = {
            "2000-02-02": {
                "XS12345678902": {
                    'date': {
                        "payment_date": "2000-02-02",
                        "record_date": "2000-01-25",
                        "ex_date": "2000-01-24"
                    },
                    'cashflow': {
                        'total': 0.05 / 12 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                            'variable_coupon_interest_component': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                            'total_coupon_interest': 0.05 / 12 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                        },
                        'principal': {
                            'redemption_principal': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                            'amortising': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                            'total_principal': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"]
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
                        'total': 0.05 / 12  * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12  * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                            'variable_coupon_interest_component': 0 * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                            'total_coupon_interest': 0.05 / 12  * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                        },
                        'principal': {
                            'redemption_principal': 0 * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                            'amortising': 0 * portfolio_holdings["holdings"]["XS12345678901"]["volume"],
                            'total_principal': 0 * portfolio_holdings["holdings"]["XS12345678901"]["volume"]
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
                        'total': 0.05 / 12  * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                        'coupon_interest': {
                            'fixed_coupon_interest_component': 0.05 / 12  * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                            'variable_coupon_interest_component': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                            'total_coupon_interest': 0.05 / 12  * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                        },
                        'principal': {
                            'redemption_principal': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                            'amortising': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                            'total_principal': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"]
                        }
                    }
                }   
            }
        }
    
        result = get_portfolio_future_cashflows(portfolio_holdings, security_lifetime_cashflow_object)
    
        self.assertDictEqual(result, expected_result)
        
    
class PortfolioHistoricalCashflowsTest(unittest.TestCase):
        
    def test_portfolio_holdings_not_dict(self):
            
        pricing_date = _default_date("2000-08-01")    
            
        portfolio_holdings = "not a dict"
        
        security_lifetime_cashflow_object = {
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
                    
        with self.assertRaises(Exception) as context:
            get_portfolio_historical_cashflows(
                pricing_date,
                portfolio_holdings,
                security_lifetime_cashflow_object
            )
        self.assertEqual(context.exception.args[0], "portfolio_holdings_index input must be of type Dict.")
    
    def test_security_cashflows_not_dict(self):
        
        pricing_date = _default_date("2000-08-01")
        
        security_lifetime_cashflow_object = "not a dict"
        
        portfolio_holdings_index = {
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
        
        with self.assertRaises(Exception) as context:
            get_portfolio_historical_cashflows(
                pricing_date,
                portfolio_holdings_index,
                security_lifetime_cashflow_object
            )
        self.assertEqual(context.exception.args[0], "security_cashflows_object input must be of type Dict.")
        
    def test_portfolio_holdings_empty(self):
        
        pricing_date = _default_date("2000-08-01")
        
        portfolio_holdings = {}
        
        security_lifetime_cashflow_object = {
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
                   
        with self.assertRaises(Exception) as context:
            get_portfolio_historical_cashflows(
                pricing_date,
                portfolio_holdings,
                security_lifetime_cashflow_object
            )
        self.assertEqual(context.exception.args[0], "portfolio_holdings_index input must not be empty.")
        
    def test_security_cashflows_empty(self):
        
        pricing_date = _default_date("2000-08-01")
        
        security_lifetime_cashflow_object = {}
        
        portfolio_holdings_index = {
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
                
        with self.assertRaises(Exception) as context:
            get_portfolio_historical_cashflows(
                pricing_date,
                portfolio_holdings_index,
                security_lifetime_cashflow_object
            )
        self.assertEqual(context.exception.args[0], "security_cashflows_object input must not be empty.")
            
    def test_portfolio_historical_cashflows(self):
        
        pricing_date = _default_date("2001-08-01")
        
        portfolio_holdings_index = {
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
        
        security_lifetime_cashflow_object = {
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
    
        expected_result = {
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
        
        result = get_portfolio_historical_cashflows(pricing_date, portfolio_holdings_index, security_lifetime_cashflow_object)
        
        self.assertEqual(result, expected_result)

class PortfolioCashflowGivenHoldingsTest(unittest.TestCase):
    
    def test_get_cashflow_given_holdings(self):
        
        security_id = "XS12345678901"
        
        portfolio_holdings = {
            "date": "2000-01-24",
            "holdings": {
                "XS12345678901": {
                    "volume": 100000.0
                },
                "XS12345678902": {
                    "volume": 100000.0
                }
            }
        }
        
        security_cashflow = {
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
        }
        
        key_mapping = [
            ('total', 'total'),
            ('fixed_coupon_interest_component', 'coupon_interest.fixed_coupon_interest_component'),
            ('variable_coupon_interest_component', 'coupon_interest.variable_coupon_interest_component'),
            ('total_coupon_interest', 'coupon_interest.total_coupon_interest'),
            ('redemption_principal', 'principal.redemption_principal'),
            ('amortising', 'principal.amortising'),
            ('total_principal', 'principal.total_principal'),
        ]
        
        expected = {
            'date': {
                "payment_date": "2000-03-02",
                "record_date": "2000-02-25",
                "ex_date": "2000-02-22"
            },
            'cashflow': {
                'total': 0.05 / 12  * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                'coupon_interest': {
                    'fixed_coupon_interest_component': 0.05 / 12  * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                    'variable_coupon_interest_component': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                    'total_coupon_interest': 0.05 / 12  * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                },
                'principal': {
                    'redemption_principal': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                    'amortising': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"],
                    'total_principal': 0 * portfolio_holdings["holdings"]["XS12345678902"]["volume"]
                }
            }
        }
        
        result = _get_cashflow_given_holdings(security_cashflow, security_id, portfolio_holdings, key_mapping)
        
        self.assertEqual(result, expected)
        