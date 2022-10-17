import unittest
import datetime

from src.analytics.security.security_risk import (calculate_macaulay_duration)
from src.analytics.utils.cashflow import (generate_fixed_cashflows)

class SecurityRiskTestCase(unittest.TestCase):

   def test_calculate_macaulay_duration_fixed_annual(self):      
      # 10-Year | 8% annual coupon bond | yield 10.40% | price 85.503075
      starting_date = datetime.datetime(2000, 1, 1)
      ending_date = datetime.datetime(2010, 1, 1)
      yield_to_final = 0.1040
      periods_per_year = 1
      coupon_rate = 0.08
      face_value = 100
      present_value = 85.503075

      cashflows = generate_fixed_cashflows(starting_date, ending_date, periods_per_year, face_value, coupon_rate)

      result = calculate_macaulay_duration(starting_date, dirty_price=present_value, cashflows=cashflows, yield_to_final=yield_to_final) 

      self.assertEqual(round(result), round(7.0029))

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

      cashflows = generate_fixed_cashflows(starting_date, ending_date, periods_per_year, face_value, coupon_rate)

      result = calculate_macaulay_duration(settlement_date, dirty_price=present_value, cashflows=cashflows, yield_to_final=yield_to_final)

      self.assertEqual(result, 12.621268)


