import unittest
import datetime
from analytics.utils.cashflow import (
    match_cashflow_to_discount_curve, 
    sum_cashflows, 
    trim_cashflows_after_workout
)

from ..helper.testConstants import MOCK_CASHFLOW_AND_DISCOUNT_CURVE, MOCK_DISCOUNT_CURVE, MOCK_SECURITY_CASHFLOW_ARRAY

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


