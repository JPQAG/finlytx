from datetime import datetime
import unittest
import pandas as pd
from typing import Any, Dict, List

from src.analytics.utils.cashflow import (
    generate_cashflows
)

from src.analytics.utils.date_time import (
    _default_date
)

from src.analytics.utils.pricing import (
    get_negative_accrued_interest,
    get_accrued_interest,
    get_pricing_history
)

class AccruedInterestTestCase(unittest.TestCase):
    
    def test_get_negative_accrued_interest(self):
        
        self.assertEqual(
            get_negative_accrued_interest(
                pricing_date = datetime.strptime("2000-01-25", "%Y-%m-%d"),
                coupon_period_start_date = datetime.strptime("2000-01-01", "%Y-%m-%d"),
                coupon_period_end_date = datetime.strptime("2000-01-31", "%Y-%m-%d"),
                ex_date = datetime.strptime("2000-01-25", "%Y-%m-%d"),
                coupon_payment_amount = 31.00
            ),
            -7.00
        )
        
        self.assertEqual(
            get_negative_accrued_interest(
                pricing_date = datetime.strptime("2000-01-31", "%Y-%m-%d"),
                coupon_period_start_date = datetime.strptime("2000-01-01", "%Y-%m-%d"),
                coupon_period_end_date = datetime.strptime("2000-01-31", "%Y-%m-%d"),
                ex_date = datetime.strptime("2000-01-25", "%Y-%m-%d"),
                coupon_payment_amount = 31.00
            ),
            -1.00
        )
        
        self.assertEqual(
            get_negative_accrued_interest(
                pricing_date = datetime.strptime("2000-01-30", "%Y-%m-%d"),
                coupon_period_start_date = datetime.strptime("2000-01-01", "%Y-%m-%d"),
                coupon_period_end_date = datetime.strptime("2000-01-31", "%Y-%m-%d"),
                ex_date = datetime.strptime("2000-01-25", "%Y-%m-%d"),
                coupon_payment_amount = 31.00
            ),
            -2.00
        )
        
    def test_get_accrued_interest(self):
        
        coupon_period_start_date = datetime.strptime("2000-01-01", "%Y-%m-%d")
        coupon_period_end_date = datetime.strptime("2000-01-31", "%Y-%m-%d")
        record_date = datetime.strptime("2000-01-25", "%Y-%m-%d")
        coupon_payment_amount = 31.00
        
        self.assertTrue(
            get_accrued_interest(
                datetime.strptime("2000-01-15", "%Y-%m-%d"), 
                coupon_period_start_date,
                coupon_period_end_date,
                record_date,
                coupon_payment_amount
            ),
            15.00
        )
        
        self.assertTrue(
            get_accrued_interest(
                datetime.strptime("2000-01-28", "%Y-%m-%d"), 
                coupon_period_start_date,
                coupon_period_end_date,
                record_date,
                coupon_payment_amount
            ),
            -4.0
        )
        
        self.assertTrue(
            get_accrued_interest(
                datetime.strptime("2000-01-28", "%Y-%m-%d"), 
                coupon_period_start_date,
                coupon_period_end_date,
                record_date,
                coupon_payment_amount
            ),
            -4.0
        )
    
    def test_get_accrued_interest_date_input_incorrect(self):
        
        coupon_period_start_date = datetime.strptime("2000-01-01", "%Y-%m-%d")
        coupon_period_end_date = datetime.strptime("2000-01-31", "%Y-%m-%d")
        record_date = datetime.strptime("2000-01-25", "%Y-%m-%d")
        coupon_payment_amount = 31.00
        
        with self.assertRaises(Exception) as context:
            get_accrued_interest(
                datetime.strptime("1990-01-01", "%Y-%m-%d"),
                coupon_period_start_date,
                coupon_period_end_date,
                record_date,
                coupon_payment_amount
            )
        self.assertEqual(context.exception.args[0], "pricing_date must be >= period_start and <= period_end.")
        
        
        with self.assertRaises(Exception) as context:
            get_accrued_interest(
                datetime.strptime("2000-01-01", "%Y-%m-%d"),
                coupon_period_start_date,
                coupon_period_end_date,
                datetime.strptime("1990-01-10", "%Y-%m-%d"),
                coupon_payment_amount
            )
        self.assertEqual(context.exception.args[0], "record_date must be >= period_start and <= period_end.")

class PriceHistoryTestCase(unittest.TestCase):

    def test_get_pricing_history(self):
        
        coupon_rate_periodic = 5/12/100
        
        issue_date = "2000-01-01"

        date_range = pd.bdate_range(issue_date, '2000-12-25')
        
        cashflow_input = generate_cashflows(
            start_date=_default_date(issue_date),
            end_date=_default_date("2001-01-01"),
            cashflow_freq="M",
            face_value=100.00,
            coupon_rate_or_margin=0.05
        )
                
        price_history_input = [
            {
                "date": date,
                "price": 100
            }
            for date
            in date_range
        ]
        
        expected = []
        
        result = get_pricing_history(
            issue_date,
            price_history_input,
            cashflow_input
        )
        
        self.assertEqual(expected, result)
        
        
        
        