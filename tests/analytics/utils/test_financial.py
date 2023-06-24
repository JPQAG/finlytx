import datetime
import unittest

from finx.analytics.utils.financial import (calculate_daily_returns,
                                           discount_rate,
                                           discount_rate_of_cashflows,
                                           future_value, implied_forward_rate, present_value,
                                           present_value_of_cashflows)
from tests.analytics.helper.testConstants import (MOCK_DISCOUNT_CURVE,
                                                  MOCK_SECURITY_CASHFLOW_ARRAY,
                                                  MOCK_SECURITY_PRICING_SERIES,
                                                  MOCK_SECURITY_RETURNS)


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

class ImpliedForwardTestCase(unittest.TestCase):

    def test_implied_forward_rate_incorrect_input_type(self):
        settlement = {
            "tenor": "STRING NOT FLOAT",
            "rate": 0.0365
        }

        workout = {
            "tenor": 4.00,
            "rate": 0.0418
        }

        with self.assertRaises(Exception) as context:
            implied_forward_rate(
                settlement = settlement,
                workout = workout,
                freq="SA"
            )
        self.assertEqual(context.exception.args[0], "'STRING NOT FLOAT' input must be of type float.")

    def test_implied_forward_rate_incorrect_freq(self):

        settlement = {
            "tenor": 3.00,
            "rate": 0.0365
        }

        workout = {
            "tenor": 4.00,
            "rate": 0.0418
        }

        with self.assertRaises(Exception) as context:
            implied_forward_rate(
                settlement = settlement,
                workout = workout,
                freq="PQT"
            )    
        self.assertEqual(context.exception.args[0], "PQT is not in dict_keys(['A', 'SA', 'Q', 'M'])")

    def test_implied_forward_rate(self):
        """Implied forward rate.

        CFA 2021 - Level 1 - Quantitative Methods - Page 555
        
        Suppose that the yields-to-maturity on three-year and four-year zero-coupon bonds
        are 3.65% and 4.18% respectively, stated on a semiannual bond basis. An analyst
        would like to know the "3Y1Y" implied forward rate, which is the implied
        one-year forward yield three years into the future. 
        """
        settlement = {
            "tenor": 3.00,
            "rate": 0.0365
        }

        workout = {
            "tenor": 4.00,
            "rate": 0.0418
        }

        result = implied_forward_rate(
            settlement = settlement,
            workout = workout,
            freq="SA"
        )

        expected = 0.05778

        self.assertEqual(round(result, 5), expected)


