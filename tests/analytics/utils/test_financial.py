import unittest
import datetime

from analytics.utils.financial import present_value, present_value_of_cashflows, future_value
from ..helper.testConstants import MOCK_SECURITY_CASHFLOW_ARRAY

class FinancialTestCase(unittest.TestCase):
    def test_present_value(self):
       
        pricing_date = datetime.datetime(2000,1,1)
        cashflow_date = datetime.datetime(2006,1,1)
        discount_rate = 0.08
        future_value = 100000
        
        result = present_value(pricing_date, cashflow_date, future_value, discount_rate)
        
        self.assertEqual(round(result, 2), 63016.96)
        
    def test_present_value_of_cashflows(self):
        
        pricing_date = datetime.datetime(2000, 1, 1)
        cashflows = MOCK_SECURITY_CASHFLOW_ARRAY
        
        result = present_value_of_cashflows(pricing_date, cashflows)
        
        self.assertEqual(round(result, 2), 15036.46)

    def test_future_value(self):

        pricing_date = datetime.datetime(2000,1,1)
        cashflow_date = datetime.datetime(2006,1,1)
        discount_rate = 0.08
        present_value = 63016.96
        
        result = future_value(pricing_date, cashflow_date, present_value, discount_rate)
        
        self.assertEqual(round(result, 2), 100000)
        
        