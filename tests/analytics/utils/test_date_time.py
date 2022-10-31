import unittest
from datetime import datetime

from src.analytics.utils.date_time import (
    _monthly_range,
    generate_date_range,
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

class DateTimeRangeTestCase(unittest.TestCase):

    def test_generate_date_range(self):

        # Test Cases 
        ## In advance, Annual
        self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2002-01-01", freq_input="A", arrears=False), ["2000-01-01","2001-01-01"])
        ## In arrears, Annual
        self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2002-01-01", freq_input="A", arrears=True), ["2001-01-01","2002-01-01"])

    def test_generate_date_range_start_end(self):
        # Cases
        # Start Date late
        self.assertEqual(generate_date_range(start_date="2000-01-02", end_date="2003-01-01", freq_input="A", arrears=True), ["2001-01-02","2002-01-02"])
        # End Date late
        self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2003-01-02", freq_input="A", arrears=True), ["2001-01-01","2002-01-01","2003-01-01"])
        # Start equals end
        self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2001-01-01", freq_input="A", arrears=False), ["2000-01-01"])
        # Start after end
        with self.assertRaises(Exception) as context:
            generate_date_range(start_date="2003-01-01", end_date="2000-01-01")
            self.assertTrue("start_date after end_date" in context.exception)

    def test_generate_date_range_freq(self):
        ## Annual
        # self.assertEqual(generate_date_range(start_date="2000-01-10", end_date="2003-01-10", freq_input="A", arrears=True), ["2001-01-10","2002-01-10","2003-01-10"])
        ## Semi-Annual
        # self.assertEqual(generate_date_range(start_date="2000-01-10", end_date="2002-01-10", freq_input="SA", arrears=True), ["2000-07-10","2001-01-10","2001-07-10","2002-01-10"])
        ## Semi-Annual
        self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2002-01-01", freq_input="SA", arrears=True), ["2000-07-01","2001-01-01","2001-07-01","2002-01-01"])
        ## Quarterly
        # self.assertEqual(generate_date_range(start_date="2000-01-10", end_date="2002-01-10", freq_input="Q", arrears=True), ["2000-04-10","2000-07-10","2000-10-10","2001-01-10","2001-04-10","2001-07-10","2001-10-10","2002-01-10"])
        ## Monthly
        # self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2000-06-01", freq_input="M", arrears=True), ["2000-02-01","2000-03-01","2000-04-01","2000-05-01","2000-06-01"])

    def test_generate_date_range_arrears(self):
        
        self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2003-01-01", freq_input="A", arrears=True), ["2001-01-01","2002-01-01","2003-01-01"])
        self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2001-01-01", freq_input="A", arrears=False), ["2000-01-01","2001-01-01", "2002-01-01"])

        self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2000-01-04", freq_input="M", arrears=True), ["2000-02-01","2000-03-01","2000-04-01"])
        self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2000-01-04", freq_input="M", arrears=False), ["2000-01-01","2000-02-01","2000-03-01"])

    def test_monthly_range(self):

        self.assertEqual(_monthly_range(start_date="2000"))