import unittest
import datetime

from analytics.utils.date_time import years_between_dates


class DateTimeTestCase(unittest.TestCase):
    def test_years_between_dates(self):

        start_date = datetime.datetime(2000, 1, 1)
        end_date = datetime.datetime(2001, 1, 1)

        self.assertEqual(years_between_dates(start_date, end_date), 1)
