import unittest

from src.analytics.security.security_return import (
    get_daily_return
)

class SecurityReturnTestCase(unittest.TestCase):
    
    def test_get_daily_return_not_float_input_previous(self):
        
        with self.assertRaises(Exception) as context:
            get_daily_return(
                "Not a float",
                100.00
            )
        self.assertEqual(context.exception.args[0], "Input prices must be of type float.")
        
    def test_get_daily_return_not_float_input_close(self):
        with self.assertRaises(Exception) as context:
            get_daily_return(
                100.00,
                "Not a float"
            )
        self.assertEqual(context.exception.args[0], "Input prices must be of type float.")
    
    def test_get_daily_return(self):
        
        previous_close = 100.00
        close = 110.00
        
        expected = 0.100
        
        result = get_daily_return(previous_close, close)
        
        self.assertEqual(round(result, 3), expected)
        
    def test_get_daily_return_history(self):
        
        price_close_history = [
            {
                'date': '2000-01-01',
                'price': 100.00
            },
            {
                'date': '2000-01-02',
                'price': 101.00
            },
            {
                'date': '2000-01-03',
                'price': 100.00
            },
            {
                'date': '2000-01-04',
                'price': 102.00
            },
        ]
        
        expected = [
            {
                'date': '2000-01-01',
                'daily_return': 100.00
            },
            {
                'date': '2000-01-02',
                'daily_return': 101.00
            },
            {
                'date': '2000-01-03',
                'daily_return': 100.00
            },
            {
                'date': '2000-01-04',
                'daily_return': 102.00
            }
        ]
        
        
        