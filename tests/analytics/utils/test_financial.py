import unittest
import datetime

from src.analytics.utils.financial import (
    present_value,
    present_value_of_cashflows,
    future_value,
    discount_rate,
    discount_rate_of_cashflows,
    calculate_daily_returns
)
from tests.analytics.helper.testConstants import (
    MOCK_DISCOUNT_CURVE, 
    MOCK_SECURITY_CASHFLOW_ARRAY, 
    MOCK_SECURITY_PRICING_SERIES,
    MOCK_SECURITY_RETURNS
)


class FinancialTestCase(unittest.TestCase):
    def test_present_value(self):

        pricing_date = datetime.datetime(2000, 1, 1)
        cashflow_date = datetime.datetime(2006, 1, 1)
        discount_rate = 0.08
        future_value = 100000

        result = present_value(pricing_date, cashflow_date, future_value, discount_rate)

        self.assertEqual(round(result, 2), 62990.39)

    def test_present_value_of_cashflows(self):

        pricing_date = datetime.datetime(2000, 1, 1)
        cashflows = MOCK_SECURITY_CASHFLOW_ARRAY
        discount_curve = MOCK_DISCOUNT_CURVE

        result = present_value_of_cashflows(pricing_date, cashflows, discount_curve)

        self.assertEqual(round(result, 2), 15033.82)

    def test_future_value(self):

        pricing_date = datetime.datetime(2000, 1, 1)
        cashflow_date = datetime.datetime(2006, 1, 1)
        discount_rate = 0.08
        present_value = 63016.96

        result = future_value(pricing_date, cashflow_date, present_value, discount_rate)

        self.assertEqual(round(result, 2), 100042.18)

    def test_discount_rate(self):

        pricing_date = datetime.datetime(2000, 1, 1)
        cashflow_date = datetime.datetime(2006, 1, 1)
        present_value = 63016.96
        future_value = 100000

        result = discount_rate(pricing_date, cashflow_date, present_value, future_value)

        self.assertEqual(round(result, 2), 0.08)

    def test_discount_rate_of_cashflows(self):

        pricing_date = datetime.datetime(2000, 1, 1)
        cashflows = MOCK_SECURITY_CASHFLOW_ARRAY
        present_value = 1000

        result = discount_rate_of_cashflows(pricing_date, cashflows, present_value)

        self.assertEqual(round(result, 6), 0.781475)

    def test_calculate_daily_returns(self):
        price_series = MOCK_SECURITY_PRICING_SERIES

        result = calculate_daily_returns(price_series)

        self.assertEqual(result, MOCK_SECURITY_RETURNS)