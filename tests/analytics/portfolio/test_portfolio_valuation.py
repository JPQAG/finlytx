import unittest

from src.analytics.portfolio.portfolio_holdings import (
    get_holdings_from_trades
)

from src.analytics.portfolio.portfolio_valuation import (
    get_portfolio_valuation
)

from ..helper.testConstants import (
    MOCK_TRADES_INDEX
)

class PortfolioValuationTestCase(unittest.TestCase):
    
    def test_get_portfolio_valuation_empty_input(self):
        with self.assertRaises(Exception) as context:
            get_portfolio_valuation({},{},{})
        self.assertEqual(context.exception.args[0], "Input indices cannot be empty.")
    
    def test_get_portfolio_valuation(self):
        
        portfolio_holdings = get_holdings_from_trades(MOCK_TRADES_INDEX)
        
        price_history_index = {
            "XS12345678901": {
                "2000-01-01": {
                    "source": "mock_source",
                    "clean_price": 100.00,
                    "accrued_interest": 1.50,
                    "dirty_price": 101.50
                },
                "2000-02-01": {
                    "source": "mock_source",
                    "clean_price": 100.00,
                    "accrued_interest": 1.50,
                    "dirty_price": 101.50
                },
                "2000-03-31": {
                    "source": "mock_source",
                    "clean_price": 100.00,
                    "accrued_interest": 1.50,
                    "dirty_price": 101.50
                },
                "2000-06-30": {
                    "source": "mock_source",
                    "clean_price": 100.00,
                    "accrued_interest": 1.50,
                    "dirty_price": 101.50
                },
            },
            "XS12345678902": {
                "2000-01-01": {
                    "source": "mock_source",
                    "clean_price": 100.00,
                    "accrued_interest": 0.50,
                    "dirty_price": 101.50
                },
                "2000-02-01": {
                    "source": "mock_source",
                    "clean_price": 100.00,
                    "accrued_interest": 0.50,
                    "dirty_price": 101.50
                },
                "2000-03-31": {
                    "source": "mock_source",
                    "clean_price": 100.00,
                    "accrued_interest": 0.50,
                    "dirty_price": 101.50
                },
                "2000-06-30": {
                    "source": "mock_source",
                    "clean_price": 100.00,
                    "accrued_interest": 0.50,
                    "dirty_price": 101.50
                }
            }            
        }
        
        security_des_index = {
            ""
        }
        
        expected = {
            "2000-01-03" : {
                "date": "2000-01-03",
                "valuation": {
                    "total_volume": 100000,
                    "clean_valuation": 100000,
                    "accrued_interest": 1500,
                    "total_valuation": 101500
                },
                "holdings": {
                    "XS12345678901": {
                        "clean_price": 100.000,
                        "accrued_interest": 1.500,
                        "dirty_price": 101.500,
                        "volume": 100000,
                        "clean_valuation": 100000,
                        "accrued_interest": 1500,
                        "total_valuation": 101500
                    }
                }
            },
            "2000-02-03" : {
                "date": "2000-02-03",
                "valuation": {
                    "total_volume": 200000,
                    "clean_valuation": 200000,
                    "accrued_interest": 3000,
                    "total_valuation": 203000
                },
                "holdings": {
                    "XS12345678901": {
                        "clean_price": 100.000,
                        "accrued_interest": 1.500,
                        "dirty_price": 101.500,
                        "volume": 100000,
                        "clean_valuation": 100000,
                        "accrued_interest": 1500,
                        "total_valuation": 101500
                    },
                    "XS12345678902": {
                        "clean_price": 100.000,
                        "accrued_interest": 1.500,
                        "dirty_price": 101.500,
                        "volume": 100000,
                        "clean_valuation": 100000,
                        "accrued_interest": 1500,
                        "total_valuation": 101500
                    }
                }
            },
            "2000-04-02" : {
                "date": "2000-04-02",
                "holdings": {
                    "XS12345678901": {
                        "clean_price": 100.000,
                        "accrued_interest": 1.500,
                        "dirty_price": 101.500,
                        "volume": 100000,
                        "clean_valuation": 100000,
                        "accrued_interest": 1500,
                        "total_valuation": 101500
                    },
                    "XS12345678902": {
                        "clean_price": 100.000,
                        "accrued_interest": 1.500,
                        "dirty_price": 101.500,
                        "volume": 0,
                        "clean_valuation": 0,
                        "accrued_interest": 0,
                        "total_valuation": 0
                    }
                }
            },
            "2000-07-02" : {
                "date": "2000-07-02",
                "holdings": {
                    "XS12345678901": {
                        "clean_price": 100.000,
                        "accrued_interest": 1.500,
                        "dirty_price": 101.500,
                        "volume": 50000,
                        "clean_valuation": 50000,
                        "accrued_interest": 750,
                        "total_valuation": 50750
                    },
                    "XS12345678902": {
                        "clean_price": 100.000,
                        "accrued_interest": 1.500,
                        "dirty_price": 101.500,
                        "volume": 0,
                        "clean_valuation": 0,
                        "accrued_interest": 0,
                        "total_valuation": 0
                    }
                }
            }
        }
        
        result = get_portfolio_valuation()
        
        self.assertEqual(expected, )
        
        
        