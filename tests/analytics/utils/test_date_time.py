import unittest
from datetime import datetime

from src.analytics.utils.date_time import (
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
    """Test class for the generate_date_range function.

    Test Cases:
        test_generate_date_range
            1. Expect first date equal to start_date.
            2. Expect first date equal to start_date + 1 period.
            3. First date one day later - expect to not generate end_date.

        test_generate_date_range_start_end    
            4. End date one day later - expect to generate end_date.
            5. start_date equals end_date - expect single date equal to start_date.
            6. start_date after end_date - expect Exception *TODO: change to specific exception.

        test_generate_date_range_freq
            7. Expect quarterly dates.
            8. Expect monthly dates.
            9. Expect weekly dates.
            10. Expect daily dates.

    Args:
        unittest (_type_): _description_
    """

    def test_generate_date_range(self):

        # Test Cases 
        ## In advance, Annual
        self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2002-01-01", freq="Y", arrears=False), ["2000-01-01","2001-01-01","2002-01-01"])
        ## In arrears, Annual
        self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2002-01-01", freq="Y", arrears=True), ["2001-01-01","2002-01-01","2003-01-01"])

    def test_generate_date_range_start_end(self):
        # Cases
        # Start Date late
        self.assertEqual(generate_date_range(start_date="2000-01-02", end_date="2003-01-01", freq="A", arrears=True), ["2001-01-02","2002-01-02"])
        # End Date late
        self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2003-01-02", freq="A", arrears=True), ["2001-01-01","2002-01-01","2003-01-01"])
        # Start equals end
        self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2001-01-01", freq="A", arrears=False), ["2000-01-01"])
        # Start after end
        with self.assertRaises(Exception) as context:
            generate_date_range(start_date="2003-01-01", end_date="2000-01-01")
            self.assertTrue("start_date after end_date" in context.exception)

    def test_generate_date_range_freq(self):
        ## Quarterly
        self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2002-01-01", freq="Q", arrears=True), ["2000-04-01","2000-07-01","2000-10-01"])
        ## Monthly
        self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2002-01-01", freq="M", arrears=True), ["2000-02-01","2000-03-01","2000-04-01"])
        ## Weekly
        self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2002-01-01", freq="W", arrears=True), ["2000-01-08","2000-01-15","2003-01-22"])
        ## Daily
        self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2002-01-01", freq="D", arrears=True), ["2000-01-08","2000-01-15","2003-01-22"])

    def test_generate_date_range_arrears(self):
        pass

