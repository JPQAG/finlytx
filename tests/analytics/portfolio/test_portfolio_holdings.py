import unittest

from finx.analytics.portfolio.portfolio_holdings import (
    get_holdings_from_trades
)

from ..helper.testConstants import (
    MOCK_TRADES_INDEX
)

class PortfolioHoldingsTestCase(unittest.TestCase):
    
    def test_get_holdings_from_trades_empty_input(self):
        with self.assertRaises(Exception) as context:
            get_holdings_from_trades([])
        self.assertEqual(context.exception.args[0], "Trade history must not be empty.")
    
    def test_get_holdings_from_trades(self):
        
        trades_input = MOCK_TRADES_INDEX
        
        expected = {
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
        
        result = get_holdings_from_trades(
            trades_input
        )
        
        self.assertEqual(result, expected)