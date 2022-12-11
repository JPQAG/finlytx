import unittest

from src.analytics.security.security_return import (
    get_period_return,
    get_return_history
)

class SecurityReturnTestCase(unittest.TestCase):
    
    def test_get_period_return_not_float_input_previous(self):
        
        with self.assertRaises(Exception) as context:
            get_period_return(
                "Not a float",
                100.00
            )
        self.assertEqual(context.exception.args[0], "Input prices must be of type float.")
        
    def test_get_period_return_not_float_input_close(self):
        with self.assertRaises(Exception) as context:
            get_period_return(
                100.00,
                "Not a float"
            )
        self.assertEqual(context.exception.args[0], "Input prices must be of type float.")
    
    def test_get_period_return(self):
        
        previous_close = 100.00
        close = 110.00
        
        expected = 0.100
        
        result = get_period_return(previous_close, close)
        
        self.assertEqual(round(result, 3), expected)
    
    def test_get_return_history_empty_input(self):
        with self.assertRaises(Exception) as context:
            get_return_history(
                []
            )
        self.assertEqual(context.exception.args[0], "Input list cannot be empty.")
    
    def test_get_return_history(self):
        
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
                'start_date_close': '2000-01-01',
                'end_date_close': '2000-01-02',
                'period_return': 0.01
            },
            {
                'start_date_close': '2000-01-02',
                'end_date_close': '2000-01-03',
                'period_return': -0.0099
            },
            {
                'start_date_close': '2000-01-03',
                'end_date_close': '2000-01-04',
                'period_return': 0.02
            }
        ]
        
        result = get_return_history(price_close_history)
        
        self.assertEqual(len(result), len(expected))
        self.assertEqual(
            round(result[0]['period_return'], 4), 
            expected[0]['period_return']
        )
        self.assertEqual(
            round(result[1]['period_return'], 4), 
            expected[1]['period_return']
        )
        self.assertEqual(
            round(result[2]['period_return'], 4), 
            expected[2]['period_return']
        )
        
        
        