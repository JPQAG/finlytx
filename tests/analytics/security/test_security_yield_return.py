import unittest
import datetime

from src.analytics.security.security_yield_return import (
    yield_to_workout, 
    current_yield,
    spread_to_benchmark
)

from ..helper.testConstants import MOCK_BENCHMARK_CURVE, MOCK_SECURITY_CASHFLOW_ARRAY

class SecurityAnalysisTestCase(unittest.TestCase):
    def test_yield_to_workout(self):

        pricing_date = datetime.datetime(2000, 1, 1)
        cashflows = MOCK_SECURITY_CASHFLOW_ARRAY
        present_value = 1000
        workout_date = MOCK_SECURITY_CASHFLOW_ARRAY[-2]["date"]

        result = yield_to_workout(
            pricing_date,
            cashflows,
            present_value,
            workout_date
        )

        self.assertEqual(round(result, 6), 0.860418)

    def test_current_yield(self):

        face_value = 100
        coupon_rate = 0.05
        market_price = 100

        result = current_yield(
            face_value,
            coupon_rate,
            market_price
        )

        self.assertEqual(result, 0.05)

    def test_spread_to_benchmark(self):

        pricing_date = datetime.datetime(2000, 1, 1)
        cashflows = MOCK_SECURITY_CASHFLOW_ARRAY
        present_value = 1000
        workout_date = MOCK_SECURITY_CASHFLOW_ARRAY[-2]["date"]
        benchmark_curve = MOCK_BENCHMARK_CURVE
        interpolation_method = 'ns'

        result = spread_to_benchmark(
            pricing_date,
            cashflows,
            present_value,
            workout_date,
            benchmark_curve,
            interpolation_method
        )

        self.assertAlmostEqual(round(result, 6), 0.825989)

