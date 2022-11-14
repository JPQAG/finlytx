import unittest
import datetime
from src.analytics.utils.cashflow import (
    generate_cashflows,
    get_most_recent_cashflow,
    match_cashflow_to_discount_curve, 
    sum_cashflows, 
    trim_cashflows_after_workout,
    generate_cashflows
)
from src.analytics.utils.lookup import TIMESERIES_TIME_PERIODS

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

    def test_get_most_recent_cashflow(self):

        # Between first and second cashflow
        self.assertEqual(get_most_recent_cashflow(datetime.datetime(2001,4,1), MOCK_SECURITY_CASHFLOW_ARRAY), MOCK_SECURITY_CASHFLOW_ARRAY[0])
        # Reference date equals second cashflow date
        self.assertEqual(get_most_recent_cashflow(datetime.datetime(2002,1,1), MOCK_SECURITY_CASHFLOW_ARRAY), MOCK_SECURITY_CASHFLOW_ARRAY[1])
        # Before first cashflow throws exception
        with self.assertRaises(ValueError):
            get_most_recent_cashflow(datetime.datetime(1999,1,1), MOCK_SECURITY_CASHFLOW_ARRAY)
        # Empty cashflow array
        with self.assertRaises(ValueError):
            get_most_recent_cashflow(datetime.datetime(2001,4,1), [])

class GenerateCashflowTestCase(unittest.TestCase):

    # Test Cases
    ## Fixed
        
    def test_generate_cashflows_args_error_start_date_type_incorrect(self):

        coupon_rate_periodic = 0.05/1

        with self.assertRaises(Exception) as context:
            generate_cashflows(
                start_date = "2000-01-01",
                end_date = datetime.datetime.strptime("2000-12-01", "%Y-%m-%d"),
                cashflow_freq = "M",
                face_value = 100,
                coupon_rate = coupon_rate_periodic
            )
        self.assertEqual(context.exception.args[0], "Date arguments must be of type datetime.")

    def test_generate_cashflows_args_error_start_date_type_incorrect(self):

        coupon_rate_periodic = 0.05/1

        with self.assertRaises(Exception) as context:
            generate_cashflows(
                start_date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d"),
                end_date = "2000-12-01",
                cashflow_freq = "M",
                face_value = 100,
                coupon_rate = coupon_rate_periodic
            )
        self.assertEqual(context.exception.args[0], "Date arguments must be of type datetime.")

    def test_generate_cashflows_args_error_freq(self):
        
        coupon_rate_periodic = 0.05/1

        with self.assertRaises(Exception) as context:
            generate_cashflows(
                start_date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d"),
                end_date = datetime.datetime.strptime("2000-12-01", "%Y-%m-%d"),
                cashflow_freq = "PSQ",
                face_value = 100,
                coupon_rate = coupon_rate_periodic
            )
        self.assertEqual(context.exception.args[0], f"'PSQ' is not in {TIMESERIES_TIME_PERIODS.keys()}.")

    def test_generate_cashflows_args_error_float_type(self):
        
        coupon_rate_periodic = 0.05/1
        
        with self.assertRaises(Exception) as context:
            generate_cashflows(
                start_date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d"),
                end_date = datetime.datetime.strptime("2000-12-01", "%Y-%m-%d"),
                cashflow_freq = "M",
                face_value = "String incorrect type",
                coupon_rate = coupon_rate_periodic
            )
        self.assertEqual(context.exception.args[0], "Numeric args must be of float type.")

    def test_generate_monthly_fixed_cashflows(self):

        coupon_rate_periodic = 0.05/12

        expected = [
            {
                'date': "2000-02-01",
                'cashflow': coupon_rate_periodic * 100
            },
            {
                'date': "2000-03-01",
                'cashflow': coupon_rate_periodic * 100
            },
            {
                'date': "2000-04-01",
                'cashflow': coupon_rate_periodic * 100
            },
            {
                'date': "2000-05-01",
                'cashflow': coupon_rate_periodic * 100
            },
            {
                'date': "2000-06-01",
                'cashflow': coupon_rate_periodic * 100
            },
            {
                'date': "2000-07-01",
                'cashflow': coupon_rate_periodic * 100
            },
            {
                'date': "2000-08-01",
                'cashflow': coupon_rate_periodic * 100
            },
            {
                'date': "2000-09-01",
                'cashflow': coupon_rate_periodic * 100
            },
            {
                'date': "2000-10-01",
                'cashflow': coupon_rate_periodic * 100
            },
            {
                'date': "2000-11-01",
                'cashflow': coupon_rate_periodic * 100
            },
            {
                'date': "2000-12-01",
                'cashflow': (coupon_rate_periodic * 100) + 100
            }
        ]

        result = generate_cashflows(
            start_date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d"),
            end_date = datetime.datetime.strptime("2000-12-01", "%Y-%m-%d"),
            cashflow_freq = "M",
            face_value = 100.00,
            coupon_rate = 0.05
        )

        self.assertEqual(result, expected)

    def test_generate_annual_fixed_cashflows(self):
        
        coupon_rate_periodic = 0.05/1

        expected = [
            {
                'date': "2001-01-01",
                'cashflow': (coupon_rate_periodic * 100) + 100
            }
        ]

        result = generate_cashflows(
            start_date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d"),
            end_date = datetime.datetime.strptime("2001-01-01", "%Y-%m-%d"),
            cashflow_freq = "A",
            face_value = 100.00,
            coupon_rate = 0.05
        )

        self.assertEqual(result, expected)

    ## Floating
    ## Arrears
    ## Advance