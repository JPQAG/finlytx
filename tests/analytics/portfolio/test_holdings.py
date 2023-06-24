import unittest

from finx.analytics.portfolio.holdings import (
    get_holdings_from_trades,
    get_holdings_delta,
    get_unique_securities_from_holdings,
    get_dict_from_trade_list,
    get_unique_securities_from_trades,
    get_invested_capital_delta,
    get_holdings_by_date_and_currency
)

from finx.analytics.utils.date_time import (
    _default_date
)

from tests.analytics.helper.testConstants import (
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
        
class HoldingsDelta(unittest.TestCase):
    
    def test_get_holdings_delta(self):
        
        start_date = _default_date("2000-01-03")
        end_date = _default_date("2000-07-02")
        holdings_index = {
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
        
        expected = {
            "start_date": "2000-01-03",
            "end_date": "2000-07-02",
            "holdings_delta": {
                "XS12345678901": {
                    "volume": -50000
                },
                "XS12345678902": {
                    "volume": 0
                }
            }
        }
        
        result = get_holdings_delta(
            start_date,
            end_date,
            holdings_index
        )
        
        self.assertEqual(result, expected)
        
    def test_get_holdings_delta_two(self):
        
        start_date = _default_date("2000-01-03")
        end_date = _default_date("2000-04-02")
        holdings_index = {
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
        
        expected = {
            "start_date": "2000-01-03",
            "end_date": "2000-04-02",
            "holdings_delta": {
                "XS12345678901": {
                    "volume": 0
                },
                "XS12345678902": {
                    "volume": 0
                }
            }
        }
        
        result = get_holdings_delta(
            start_date,
            end_date,
            holdings_index
        )
        
        self.assertEqual(result, expected)
        
class HoldingsUniqueSecurities(unittest.TestCase):
    
    def test_get_unique_securities_from_holdings(self):
        holdings_index = {
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
        
        expected = ['XS12345678901', 'XS12345678902']
        
        result = get_unique_securities_from_holdings(holdings_index)
        
        self.assertEqual(result, expected)
        
class InvestedCapitalDelta(unittest.TestCase):
    
    def test_get_invested_capital_delta(self):
        
        trades_input = MOCK_TRADES_INDEX
                
        result = get_invested_capital_delta(
            _default_date("2000-01-01"),
            _default_date("2000-07-02"),
            trades_input
        )
        
        expected = {
            "start_date": "2000-01-01",
            "end_date": "2000-07-02",
            "invested_capital_delta": {
                "XS12345678901": {
                    "volume": 101500+(-100500/2)
                },
                "XS12345678902": {
                    "volume": 100500+(-101500/2)+(-101500/2)
                }
            }
        }
        
        self.assertEqual(result, expected)
        
class ConvertTradeListToDict(unittest.TestCase):
    
    def test_get_dict_from_trade_list(self):
        
        trades_input = MOCK_TRADES_INDEX
        
        expected = {
            "2000-01-01": [
                {
                    "trade_date": "2000-01-01",
                    "settlement_date": "2000-01-03",
                    "isin": "XS12345678901",
                    "original_face_value": 100.00,
                    "current_face_value": 100.00,
                    "side": "B",
                    "volume": 100000,
                    "price": 101.50
                }
            ],
            "2000-02-01": [
                {
                    "trade_date": "2000-02-01",
                    "settlement_date": "2000-02-03",
                    "isin": "XS12345678902",
                    "original_face_value": 100.00,
                    "current_face_value": 100.00,
                    "side": "B",
                    "volume": 100000,
                    "price": 100.50
                }
            ],
            "2000-03-31": [
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
                }
            ], 
            "2000-06-30": [    
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
        }
        
        result = get_dict_from_trade_list(trades_input)
        
        self.assertEqual(result, expected)

class TradesUniqueSecurites(unittest.TestCase):
    
    def test_get_unique_securities_from_trades(self):
        trades = MOCK_TRADES_INDEX
    
        result = get_unique_securities_from_trades(trades)
        
        expected = ['XS12345678901', 'XS12345678902']
        
        self.assertEqual(sorted(result), sorted(expected))
                
class GetHoldingsByDateAndCurrency(unittest.TestCase):
    
    def test_get_holdings_by_date_and_currency(self):
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
        
        security_currency_map = {
            "XS12345678901": "AUD",
            "XS12345678902": "USD"
        }
        
        expected = {
            "2000-01-03" : {
                "date": "2000-01-03",
                "holdings": {
                    "AUD": 100000,
                    "USD": 0
                }
            },
            "2000-02-03" : {
                "date": "2000-02-03",
                "holdings": {
                    "AUD": 100000,
                    "USD": 100000
                }
            },
            "2000-04-02" : {
                "date": "2000-04-02",
                "holdings": {
                    "AUD": 100000,
                    "USD": 0
                }
            },
            "2000-07-02" : {
                "date": "2000-07-02",
                "holdings": {
                    "AUD": 50000,
                    "USD": 0
                }
            }
        }
        
        result = get_holdings_by_date_and_currency(holdings, security_currency_map)
