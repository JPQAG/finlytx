import unittest
from datetime import datetime

from src.analytics.utils.date_time import (
    months_between_dates,
    years_between_dates,
    days_between_dates
)


class DateTimeTestCase(unittest.TestCase):
    def test_days_between_dates(self):

        self.assertEqual(days_between_dates(datetime(2010, 10, 1), datetime(2010, 10, 4)), 3)
        self.assertEqual(days_between_dates(datetime(2010, 9, 1), datetime(2010, 10, 1)), 30)

    def test_months_between_dates(self):

        self.assertEqual(months_between_dates(datetime(2010, 9, 1), datetime(2010, 10, 1)), 1)
        self.assertEqual(months_between_dates(datetime(2009, 10, 1), datetime(2010, 10, 1)), 12)
        self.assertEqual(months_between_dates(datetime(2009, 11, 1), datetime(2010, 10, 1)), 11)
        self.assertEqual(months_between_dates(datetime(2009, 8, 1), datetime(2010, 10, 1)), 14)

    def test_years_between_dates(self):

        self.assertEqual(years_between_dates(datetime(2009, 10, 1), datetime(2010, 10, 1)), 1.0)        
        self.assertEqual(years_between_dates(datetime(2010, 10, 1), datetime(2009, 10, 1)), -1.0)
        self.assertEqual(round(years_between_dates(datetime(2010, 10, 1), datetime(2009, 11, 1)), 4), -0.9151)
        self.assertEqual(round(years_between_dates(datetime(2010, 10, 1), datetime(2009, 8, 1)), 4), -1.1671)
        self.assertEqual(round(years_between_dates(datetime(2000, 1, 1), datetime(2010, 1, 1)), 0), 10)
