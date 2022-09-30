import unittest
import datetime
from src.analytics.utils.cashflow import (
    match_cashflow_to_discount_curve, 
    sum_cashflows, 
    trim_cashflows_after_workout,
    generate_fixed_cashflows
)

from ..helper.testConstants import MOCK_CASHFLOW_AND_DISCOUNT_CURVE, MOCK_DISCOUNT_CURVE, MOCK_SECURITY_CASHFLOW_ARRAY, MOCK_SECURITY_FIXED_RATE_CASHFLOW_ARRAY

class CashflowTestCase(unittest.TestCase):
    def test_match_cashflow_to_discount_curve(self):

        cashflows = MOCK_SECURITY_CASHFLOW_ARRAY
        discount_curve = MOCK_DISCOUNT_CURVE

        result = match_cashflow_to_discount_curve(cashflows, discount_curve)

        self.assertEqual(result, MOCK_CASHFLOW_AND_DISCOUNT_CURVE)

    def test_sum_cashflows(self):

        result = sum_cashflows(MOCK_SECURITY_CASHFLOW_ARRAY)

        self.assertEqual(result, 18000)

    def test_trim_cashflows_after_workout(self):

        cashflows = MOCK_SECURITY_CASHFLOW_ARRAY
        workout_date = MOCK_SECURITY_CASHFLOW_ARRAY[-2]['date']

        result = trim_cashflows_after_workout(cashflows, workout_date)

        self.assertEqual(result, cashflows[0:-1])

    def test_generate_fixed_cashflows(self):
        starting_date = datetime.datetime(2000,1,1)
        ending_date = datetime.datetime(2005,1,1)
        periods_per_year = 1
        face_value = 100.00
        coupon_rate = 0.10

        result = generate_fixed_cashflows(
            starting_date,
            ending_date,
            periods_per_year,
            face_value,
            coupon_rate
        )

        self.assertEqual(result, MOCK_SECURITY_FIXED_RATE_CASHFLOW_ARRAY)

    def test_get_most_recent_cashflow(self):
        
        

