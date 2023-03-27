import math
import unittest
import datetime

from finx.analytics.security.security_risk import (
   calculate_macaulay_duration,
   calculate_modified_duration,
   calculate_stdev,
   calculate_security_volatility_stdev
)
from finx.analytics.utils.cashflow import (
    generate_cashflows
)

class SecurityDurationRiskTestCase(unittest.TestCase):

   def test_calculate_macaulay_duration_fixed_annual(self):      
      # 10-Year | 8% annual coupon bond | yield 10.40% | price 85.503075
      starting_date = datetime.datetime(2000, 1, 1)
      ending_date = datetime.datetime(2010, 1, 1)
      yield_to_final = 0.1040
      periods_per_year = 1
      coupon_rate = 0.08
      face_value = 100.00
      present_value = 85.503075

      cashflows = generate_cashflows(
         start_date=starting_date,
         end_date=ending_date,
         cashflow_freq="A",
         face_value=face_value,
         coupon_rate_or_margin=coupon_rate
      )

      result = calculate_macaulay_duration(starting_date, dirty_price=present_value, cashflows=cashflows, yield_to_final=yield_to_final) 

      self.assertTrue(math.isclose(result, 7.0029, abs_tol=0.005))
      
   def test_calculate_modified_duration_fixed_annual(self):
      # 10-Year | 8% annual coupon bond | yield 10.40% | price 85.503075
      starting_date = datetime.datetime(2000, 1, 1)
      ending_date = datetime.datetime(2010, 1, 1)
      yield_to_final = 0.1040
      periods_per_year = 1
      coupon_rate = 0.08
      face_value = 100.00
      present_value = 85.503075

      cashflows = generate_cashflows(
         start_date=starting_date,
         end_date=ending_date,
         cashflow_freq="A",
         face_value=face_value,
         coupon_rate_or_margin=coupon_rate
      )
      
      macaulay_duration = calculate_macaulay_duration(starting_date, dirty_price=present_value, cashflows=cashflows, yield_to_final=yield_to_final) 
      
      modified_duration_result = calculate_modified_duration(macaulay_duration, yield_to_final/periods_per_year)
      
      self.assertEqual(round(modified_duration_result, 2), 6.34)

   def test_calculate_macaulay_duration_fixed_semiannual(self):
      # 8-Year | 6% Semiannual Payment bond | yield 6.00%
      starting_date = datetime.datetime(2000, 2, 14)
      ending_date = datetime.datetime(2027, 2, 14)
      settlement_date = datetime.datetime(2019, 4, 11)
      yield_to_final = 0.06
      periods_per_year = 2
      coupon_rate = 0.06
      face_value = 100
      present_value = 99.990423 + 0.95

      cashflows = generate_cashflows(
         start_date=starting_date,
         end_date=ending_date,
         cashflow_freq="SA",
         face_value=100.00,
         coupon_rate_or_margin=0.06
      )

      result = calculate_macaulay_duration(settlement_date, dirty_price=present_value, cashflows=cashflows, yield_to_final=yield_to_final)

      self.assertEqual(round(result, 2), 12.64)
            
   def test_calculate_modified_duration_fixed_semiannual(self):
      starting_date = datetime.datetime(2000, 2, 14)
      ending_date = datetime.datetime(2027, 2, 14)
      settlement_date = datetime.datetime(2019, 4, 11)
      yield_to_final = 0.06
      periods_per_year = 2
      coupon_rate = 0.06
      face_value = 100
      present_value = 99.990423 + 0.95

      cashflows = generate_cashflows(
         start_date=starting_date,
         end_date=ending_date,
         cashflow_freq="SA",
         face_value=100.00,
         coupon_rate_or_margin=0.06
      )
      
      macaulay_duration = calculate_macaulay_duration(settlement_date, dirty_price=present_value, cashflows=cashflows, yield_to_final=yield_to_final)
      
      modified_duration_result = calculate_modified_duration(macaulay_duration, yield_to_final/periods_per_year)
      
      self.assertEqual(round(modified_duration_result, 1), 12.3)

class securityVolatilityRiskTestCase(unittest.TestCase):
   
   def test_calculate_stdev(self):
      
      data = [7.00,5.00,4.00,9.00,12.00,45.00]
      
      expected = 15.616
      
      result = calculate_stdev(data)
      
      self.assertEqual(round(result,3), expected)
   
   def test_security_volatility(self):
      
      security_return = [
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
      
      expected = 0.01522
      
      result = calculate_security_volatility_stdev(security_return)
      
      self.assertEqual(round(result, 5), expected)


