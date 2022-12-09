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
    get_pricing_history,
    get_period_total_return,
    get_annualised_return
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
        
        end_first_period = {'date': '2000-01-31', 'clean_price': 100, 'accrued_interest': -0.013440860215053765, 'dirty_price': 99.98655913978494}
        start_second_period = {'date': '2000-02-01', 'clean_price': 100, 'accrued_interest': 0.0, 'dirty_price': 100.0}
        expected_first = {'date': '2000-01-03', 'clean_price': 100, 'accrued_interest': 0.02777777777777778, 'dirty_price': 100.02777777777777}
        expected_last = {'date': '2000-12-25', 'clean_price': 100, 'accrued_interest': -0.09408602150537634, 'dirty_price': 99.90591397849462}
        
        result = get_pricing_history(
            issue_date,
            price_history_input,
            cashflow_input
        )
        
        self.assertEqual(expected_first, result[0])
        self.assertEqual(end_first_period, result[20])
        self.assertEqual(start_second_period, result[21])
        self.assertEqual(expected_last, result[-1])
        
class HistoricalReturnsTestCase(unittest.TestCase):
    
    def test_security_return(self):
        
        issue_date = "2000-01-01"
        
        start_date = "2000-01-15"
        end_date = "2000-03-15"
        
        start_price = 100.00
        end_price = 110.00
    
        annual_coupon = 0.05
        frequency = 12
        face_value = 100
        number_of_coupons_paid = 2
            
        price_history_input = [
            {
                'date': "2000-01-15",
                'price': 100.00
            },
            {
                'date': "2000-03-15",
                'price': 110.00
            }
        ]
        
        cashflow_input = generate_cashflows(
            start_date=_default_date(issue_date),
            end_date=_default_date("2001-01-01"),
            cashflow_freq="M",
            face_value=100.00,
            coupon_rate_or_margin=0.05
        )
        
        result = get_period_total_return(
            start_date=_default_date(start_date),
            end_date=_default_date(end_date),
            price_history=price_history_input,
            security_cashflows=cashflow_input
        )
        
        expected_return = (
            (annual_coupon/frequency * face_value * number_of_coupons_paid) 
            + (end_price - start_price)
        ) / start_price
        
        self.assertEqual(expected_return, result['return']['total_return'])
        self.assertEqual(0.05/12*2, result['return']['cashflow_return'])
        self.assertEqual(0.10, result['return']['price_return'])

    def test_annualise_total_return(self):
        
        days_in_year = 365
        start_date = _default_date("2000-01-15")
        end_date = _default_date("2001-10-26")
        cumulative_return = 0.1575
        
        expected_annualised_return = 0.08560
        
        result = get_annualised_return(
            start_date=start_date,
            end_date=end_date,
            cumulative_return=cumulative_return,
            days_in_year=days_in_year
        )
        
        self.assertEqual(expected_annualised_return, round(result,5))