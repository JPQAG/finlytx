import datetime
import unittest

from src.analytics.portfolio.portfolio_holdings import (
    get_holdings_from_trades
)

from src.analytics.portfolio.portfolio_valuation import (
    get_portfolio_valuation_index,
    get_position_valuation,
    get_portfolio_valuation
)

from ..helper.testConstants import (
    MOCK_TRADES_INDEX
)

class PortfolioValuationIndexTestCase(unittest.TestCase):

    
    def test_get_portfolio_valuation_index_no_holdings_at_valuation_date(self):
        # Test the case where there are no holdings at the valuation date in the portfolio_holdings_index
        with self.assertRaises(Exception) as context:
            get_portfolio_valuation_index(
                datetime.datetime(2000,1,1),
                MOCK_TRADES_INDEX,
                {
                    "XS1234567890": {
                        "date": datetime.datetime(2000,1,1),
                        "per_original_face_value": 100,
                        "value": 101.50
                    }
                }
            )
        self.assertEqual(context.exception.args[0], "No holdings found at valuation date.")

    def test_get_portfolio_valuation_index_no_prices_at_valuation_date(self):
        # Test the case where there are no prices for any of the securities in the price_history_index on the valuation date
        with self.assertRaises(Exception) as context:
            get_portfolio_valuation_index(
                datetime.datetime(2000,1,1),
                MOCK_TRADES_INDEX,
                {
                    "XS1234567890": {
                        "date": datetime.datetime(1999,12,31),
                        "per_original_face_value": 100,
                        "value": 101.50
                    }
                }
            )
        self.assertEqual(context.exception.args[0], "No price data found for securities in portfolio at valuation date.")

    def test_get_portfolio_valuation_index_holdings_for_untracked_security(self):
        # Test the case where there are holdings for securities that are not present in the price_history_index on the valuation date
        with self.assertRaises(Exception) as context:
            get_portfolio_valuation_index(
                datetime.datetime(2000,1,1),
                MOCK_TRADES_INDEX,
                {
                    "XS1234567891": {
                        "date": datetime.datetime(2000,1,1),
                        "per_original_face_value": 100,
                        "value": 101.50
                    }
                }
            )
        self.assertEqual(context.exception.args[0], "No price data found for securities in portfolio at valuation date.")

    
    def test_get_portfolio_valuation_index_holdings_type_incorrect(self):
        with self.assertRaises(Exception) as context:
            get_portfolio_valuation_index(
                datetime.datetime(2000,1,1),
                "Not a dictionary.",
                {
                    "XS1234567890": {
                        "date": datetime.datetime(2000,1,1),
                        "per_original_face_value": 100,
                        "value": 101.50
                    }
                }
            )
        self.assertEqual(context.exception.args[0], "portfolio_holdings_index input must be of type dict.")
        
    def test_get_portfolio_valuation_index_price_history_type_incorrect(self):
        with self.assertRaises(Exception) as context:
            get_portfolio_valuation_index(
                datetime.datetime(2000,1,1),
                {
                    "XS1234567890": "Placeholder"
                },
                "Not a dictionary"
            )
        self.assertEqual(context.exception.args[0], "price_history_index input must be of type dict.")
        
    def test_get_portfolio_valuation_index_holdings_empty(self):
        with self.assertRaises(Exception) as context:
            get_portfolio_valuation_index(
                datetime.datetime(2000,1,1),
                {},
                {
                    "XS1234567890": {
                        "date": datetime.datetime(2000,1,1),
                        "per_original_face_value": 100,
                        "value": 101.50
                    }
                }
            )
        self.assertEqual(context.exception.args[0], "portfolio_holdings_index input must not be empty.")
            
    def test_get_portfolio_valuation_index(self):
        
        portfolio_holdings = {
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
        
        price_history_index = {
            "XS1234567890": {
                "2000-01-01": {
                    "date": datetime.datetime(2000,1,1),
                    "per_original_face_value": 100,
                    "currency": "AUD",
                    "base_currency_conversion_rate": 1.00,
                    "value": 100.50
                },
                "2000-02-01": {
                    "date": datetime.datetime(2000,2,1),
                    "per_original_face_value": 100,
                    "currency": "AUD",
                    "base_currency_conversion_rate": 1.00,
                    "value": 101.50
                },
                "2000-03-31": {
                    "date": datetime.datetime(2000,3,31),
                    "per_original_face_value": 100,
                    "currency": "AUD",
                    "base_currency_conversion_rate": 1.00,
                    "value": 102.50
                },
                "2000-06-30": {
                    "date": datetime.datetime(2000,6,30),
                    "per_original_face_value": 100,
                    "currency": "AUD",
                    "base_currency_conversion_rate": 1.00,
                    "value": 103.50
                }
            },
            "XS1234567891": {
                "2000-01-01": {
                    "date": datetime.datetime(2000,1,1),
                    "per_original_face_value": 100,
                    "currency": "AUD",
                    "base_currency_conversion_rate": 1.00,
                    "value": 103.50
                },
                "2000-02-01": {
                    "date": datetime.datetime(2000,2,1),
                    "per_original_face_value": 100,
                    "currency": "AUD",
                    "base_currency_conversion_rate": 1.00,
                    "value": 102.50
                },
                "2000-03-31": {
                    "date": datetime.datetime(2000,3,31),
                    "per_original_face_value": 100,
                    "currency": "AUD",
                    "base_currency_conversion_rate": 1.00,
                    "value": 101.50
                },
                "2000-06-30": {
                    "date": datetime.datetime(2000,6,30),
                    "per_original_face_value": 100,
                    "currency": "AUD",
                    "base_currency_conversion_rate": 1.00,
                    "value": 100.50
                },
            }            
        }
                
        expected = {
            "2000-01-03" : {
                "date": datetime.datetime(2000,1,3),
                "valuation": {
                    "total_valuation": {
                        "AUD": 100500
                    },
                    "position_valuation": {
                        "XS12345678901": {
                            "currency": "AUD",
                            "volume": 100000,
                            "price": {
                                "date": datetime.datetime(2000,1,1),
                                "per_original_face_value": 100,
                                "currency": "AUD",
                                "base_currency_conversion_rate": 1.00,
                                "value": 100.50
                            },
                            "valuation": 100500.00
                        }
                    }
                }
            },
            "2000-02-03" : {
                "date": datetime.datetime(2000,2,3),
                "valuation": {
                    "total_valuation": {
                        "AUD": 204000,
                    },
                    "position_valuation": {
                        "XS1234567890": {
                            "currency": "AUD",
                            "volume": 100000,
                            "price": {
                                "date": datetime.datetime(2000,2,1),
                                "per_original_face_value": 100,
                                "currency": "AUD",
                                "base_currency_conversion_rate": 1.00,
                                "value": 101.50
                            },
                            "valuation": 101500.00
                        },
                        "XS1234567891": {
                            "currency": "AUD",
                            "volume": 100000,
                            "price": {
                                "date": datetime.datetime(2000,2,1),
                                "per_original_face_value": 100,
                                "currency": "AUD",
                                "base_currency_conversion_rate": 1.0,
                                "value": 102.500
                            },
                            "valuation": 102500
                        }
                    }
                }
            },
            "2000-04-02" : {
                "date": datetime.datetime(2000,4,2),
                "valuation": {
                    "total_valuation": {
                        "AUD": 102500,
                    },
                    "position_valuation": {
                        "XS1234567890": {
                            "currency": "AUD",
                            "volume": 100000,
                            "price": {
                                "date": datetime.datetime(2000,3,31),
                                "per_original_face_value": 100,
                                "currency": "AUD",
                                "base_currency_conversion_rate": 1.00,
                                "value": 102.50
                            },
                            "valuation": 102500.00
                        },
                        "XS1234567891": {
                            "currency": "AUD",
                            "volume": 0,
                            "price": {
                                "date": datetime.datetime(2000,3,31),
                                "per_original_face_value": 100,
                                "currency": "AUD",
                                "base_currency_conversion_rate": 1.0,
                                "value": 101.500
                            },
                            "valuation": 0
                        }
                    }
                }
            },
            "2000-07-02" : {
                "date": datetime.datetime(2000,7,2),
                "valuation": {
                    "total_valuation": {
                        "AUD": 102500,
                    },
                    "position_valuation": {
                        "XS1234567890": {
                            "currency": "AUD",
                            "volume": 50000,
                            "price": {
                                "date": datetime.datetime(2000,6,30),
                                "per_original_face_value": 100,
                                "currency": "AUD",
                                "base_currency_conversion_rate": 1.00,
                                "value": 103.50
                            },
                            "valuation": 102500.00
                        },
                        "XS1234567891": {
                            "currency": "AUD",
                            "volume": 0,
                            "price": {
                                "date": datetime.datetime(2000,6,30),
                                "per_original_face_value": 100,
                                "currency": "AUD",
                                "base_currency_conversion_rate": 1.0,
                                "value": 100.500
                            },
                            "valuation": 0
                        }
                    }
                }
            }
        }
        
        self.assertEqual(
            get_portfolio_valuation_index(
                datetime.datetime(2000,10,1),
                portfolio_holdings,
                price_history_index
            ), 
            expected
        )
        
class PortfolioValuationTestCase(unittest.TestCase):
    
    def test_get_portfolio_valuation_pricing_date_input_type_incorrect(self):
        with self.assertRaises(Exception) as context:
            get_portfolio_valuation(
                "01-02-2022",
                {
                    "XS1234567890": {}
                },
                {
                    "XS1234567890": {
                        "date": datetime.datetime(2000,1,1),
                        "per_original_face_value": 100,
                        "value": 101.50
                    }
                }
            )
        self.assertEqual(context.exception.args[0], "pricing_date input must be of type datetime.datetime.")
        
    def test_get_portfolio_valuation_holding_input_incorrect(self):
        with self.assertRaises(Exception) as context:
            get_portfolio_valuation(
                datetime.datetime(2000,1,1),
                "Not a dictionary",
                {
                    "XS1234567890": {
                        "date": datetime.datetime(2000,1,1),
                        "per_original_face_value": 100,
                        "value": 101.50
                    }
                }
            )
        self.assertEqual(context.exception.args[0], "holdings input must be of type dict.")
        
    def test_get_portfolio_valuation_pricing_input_incorrect(self):
        with self.assertRaises(Exception) as context:
            get_portfolio_valuation(
                datetime.datetime(2000,1,1),
                {
                    "XS1234567890": {}
                },
                "Not a dictionary",
            )
        self.assertEqual(context.exception.args[0], "pricing input must be of type dict.")
        
    def test_get_portfolio_valuation_no_holdings(self):
        with self.assertRaises(Exception) as context:
            get_portfolio_valuation(
                datetime.datetime(2000,1,1),
                {},
                {
                    "XS1234567890": {
                        "date": datetime.datetime(2000,1,1),
                        "per_original_face_value": 100,
                        "value": 101.50
                    }
                }
            )
        self.assertEqual(context.exception.args[0], "holdings must not be empty.")
        
    def test_get_portfolio_valuation_single_currency_single_holding(self):
        # Single Holding
        # Multiple Holding
        # No prices
        # One holding with no prices
        # Differing Currency
        
        self.assertEqual(
            get_portfolio_valuation(
                datetime.datetime(2000,1,1),
                {
                    "XS1234567890": {
                        "volume": 100000
                    }
                },
                {
                    "XS1234567890": {
                        "date": datetime.datetime(2000,1,1),
                        "per_original_face_value": 100,
                        "currency": "AUD",
                        "base_currency_conversion_rate": 1.00,
                        "value": 101.50
                    }
                }
            ), 
            {
                "date": datetime.datetime(2000,1,1),
                "valuation": {
                    "total_valuation": {
                        "AUD": 101500
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
                        }
                    }
                }
            }
        )
        
    def test_get_portfolio_valuation_multi_currency_multi_holdings(self):
        self.assertEqual(
            get_portfolio_valuation(
                datetime.datetime(2000,1,1),
                {
                    "XS1234567890": {
                        "volume": 100000
                    },
                    "XS1234567891": {
                        "volume": 100000
                    }
                },
                {
                    "XS1234567890": {
                        "date": datetime.datetime(2000,1,1),
                        "per_original_face_value": 100,
                        "currency": "AUD",
                        "base_currency_conversion_rate": 1.00,
                        "value": 101.50
                    },
                    "XS1234567891": {
                        "date": datetime.datetime(2000,1,1),
                        "per_original_face_value": 100,
                        "currency": "USD",
                        "base_currency_conversion_rate": 0.75,
                        "value": 101.50
                    }
                }
            ), 
            {
                "date": datetime.datetime(2000,1,1),
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
        )
        
    def test_get_portfolio_valuation_multi_currency_multi_holdings_missing_price(self):
        
        self.assertEqual(
            get_portfolio_valuation(
                datetime.datetime(2000,1,1),
                {
                    "XS1234567890": {
                        "volume": 100000
                    },
                    "XS1234567891": {
                        "volume": 100000
                    }
                },
                {
                    "XS1234567890": {
                        "date": datetime.datetime(2000,1,1),
                        "per_original_face_value": 100,
                        "currency": "AUD",
                        "base_currency_conversion_rate": 1.00,
                        "value": 101.50
                    }
                }
            ), 
            {
                "date": datetime.datetime(2000,1,1),
                "valuation": {
                    "total_valuation": {
                        "AUD": 101500,
                        "N/A": -0.0
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
                            "currency": "N/A",
                            "volume": 100000,
                            "price": {
                                "date": datetime.datetime(2000,1,1),
                                "per_original_face_value": -1.0,
                                "currency": "N/A",
                                "base_currency_conversion_rate": 1.0,
                                "value": 0
                            },
                            "valuation": -0.0
                        }
                    }
                }
            }
        )  
            
class PositionValuationTestCase(unittest.TestCase):
    
    def test_get_position_valuation_pricing_date_input_type_error(self):
        
        with self.assertRaises(Exception) as context:
            get_position_valuation(
                "01-02-2022",
                {
                    "volume": 100000
                },
                {
                    "date": datetime.datetime(2000, 1, 1),
                    "per_original_face_value": 100,
                    "value": 101.50
                }
            )
        self.assertEqual(context.exception.args[0], "pricing_date input must be of type datetime.datetime.")
    
    def test_get_position_valuation_holding_input_type_error(self):
        with self.assertRaises(Exception) as context:
            get_position_valuation(
                datetime.datetime(2000, 1, 1),
                "Not an object",
                {
                    "date": datetime.datetime(2000, 1, 1),
                    "per_original_face_value": 100,
                    "value": 101.50
                }
            )
        self.assertEqual(context.exception.args[0], "holding input must be of type dict.")
        
    def test_get_position_valuation_price_input_type_error(self):
        with self.assertRaises(Exception) as context:
            get_position_valuation(
                datetime.datetime(2000, 1, 1),
                {
                    "volume": 100000
                },
                "Not an object"
            )
        self.assertEqual(context.exception.args[0], "price object input must be of type dict.")
        
    def test_get_position_valuation_price_date_after_holding_date(self):
        with self.assertRaises(Exception) as context:
            get_position_valuation(
                datetime.datetime(2000, 1, 1),
                {
                    "volume": 100000
                },
                {
                    "date": datetime.datetime(2000, 1, 2),
                    "per_original_face_value": 100,
                    "value": 101.50
                }
            )
        self.assertEqual(context.exception.args[0], "price object date must be on or before pricing date.")
       
    def test_get_position_valuation_hoildings_dict_empty(self):
        with self.assertRaises(Exception) as context:
            get_position_valuation(
                datetime.datetime(2000, 1, 1),
                {},
                {
                    "date": datetime.datetime(2000, 1, 1),
                    "per_original_face_value": 100,
                    "value": 101.50
                }
            )
        self.assertEqual(context.exception.args[0], "Holdings dictionary cannot be empty.")
        
    def test_get_position_valuation(self):
        
        self.assertEqual(
            get_position_valuation(
                datetime.datetime(2000, 1, 1),
                {
                    "volume": 100000
                },
                {
                    "date": datetime.datetime(2000, 1, 1),
                    "per_original_face_value": 100,
                    "value": 101.50
                }
            ), 
            101500
        )
        
        self.assertEqual(
            get_position_valuation(
                datetime.datetime(2000, 1, 1),
                {
                    "volume": 0
                },
                {
                    "date": datetime.datetime(2000, 1, 1),
                    "per_original_face_value": 100,
                    "value": 101.50
                }
            ), 
            0
        )
        
        self.assertEqual(
            get_position_valuation(
                datetime.datetime(2000, 1, 1),
                {
                    "volume": 100000
                },
                {
                    "date": datetime.datetime(2000, 1, 1),
                    "per_original_face_value": 100,
                    "value": 0
                }
            ), 
            0
        ) 
        
        