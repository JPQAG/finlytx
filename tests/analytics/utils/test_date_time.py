import unittest
from datetime import datetime
import pandas as pd

from src.analytics.utils.date_time import (
    _annual_range,
    _default_date,
    _generate_pd_date_range,
    _get_n_monthly,
    _mid_month_adj,
    _monthly_range,
    generate_date_range,
    months_between_dates,
    years_between_dates,
    days_between_dates
)
from src.analytics.utils.lookup import TIMESERIES_TIME_PERIODS


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
        self.assertListEqual(
            generate_date_range(start_date=_default_date("2000-01-01"), end_date=_default_date("2002-01-01"), freq_input="A", arrears=False),
            ["2000-01-01","2001-01-01"]
        )
        ## In arrears, Annual
        self.assertListEqual(
            generate_date_range(start_date=_default_date("2000-01-01"), end_date=_default_date("2002-01-01"), freq_input="A", arrears=True),
            ["2001-01-01","2002-01-01"]
        )
        # self.assertEqual(generate_date_range(start_date="2000-01-01", end_date="2002-01-01", freq_input="A", arrears=True), ["2001-01-01","2002-01-01"])

    def test_generate_date_range_start_end(self):
        # Cases
        # Start Date late
        self.assertListEqual(
            generate_date_range(start_date=_default_date("2000-01-02"), end_date=_default_date("2003-01-01"), freq_input="A", arrears=True),
            ["2001-01-02","2002-01-02"]
        )
        # End Date late
        self.assertListEqual(
            generate_date_range(start_date=_default_date("2000-01-01"), end_date=_default_date("2003-01-01"), freq_input="A", arrears=True),
            ["2001-01-01","2002-01-01","2003-01-01"]
        )
        # Start equals end
        self.assertListEqual(
            generate_date_range(start_date=_default_date("2000-01-01"), end_date=_default_date("2000-01-01"), freq_input="A", arrears=True),
            []
        )
        # Start after end
        with self.assertRaises(Exception) as context:
            generate_date_range(start_date="2003-01-01", end_date="2000-01-01")
        self.assertTrue(context.exception.args[0], "start_date is after end_date")

    def test_generate_date_range_freq(self):
        ## Annual
        self.assertListEqual(
            generate_date_range(start_date=_default_date("2000-01-10"), end_date=_default_date("2003-01-10"), freq_input="A", arrears=True),
            ["2001-01-10","2002-01-10","2003-01-10"]
        )
        ## Semi-Annual
        self.assertListEqual(
            generate_date_range(start_date=_default_date("2000-01-01"), end_date=_default_date("2002-01-01"), freq_input="SA", arrears=True),
            ["2000-07-01","2001-01-01","2001-07-01","2002-01-01"]
        )
        ## Quarterly
        self.assertListEqual(
            generate_date_range(start_date=_default_date("2000-01-10"), end_date=_default_date("2002-01-10"), freq_input="Q", arrears=True),
            ["2000-04-10","2000-07-10","2000-10-10","2001-01-10","2001-04-10","2001-07-10","2001-10-10","2002-01-10"]
        )
        ## Monthly
        self.assertListEqual(
            generate_date_range(start_date=_default_date("2000-01-01"), end_date=_default_date("2000-06-01"), freq_input="M", arrears=True),
            ["2000-02-01","2000-03-01","2000-04-01","2000-05-01","2000-06-01"]
        )

    def test_generate_date_range_arrears(self):

        with self.assertRaises(Exception) as context:
            generate_date_range(
                _default_date("2001-01-01"),
                _default_date("2000-01-01"),
                "A"
            )
        self.assertEqual(context.exception.args[0], "start_date is after end_date")

        with self.assertRaises(Exception) as context:
            generate_date_range(
                "2000-01-01",
                _default_date("2001-01-01")
            )
        self.assertEqual(context.exception.args[0], "start_date must be of type datetime.datetime")

        with self.assertRaises(Exception) as context:
            generate_date_range(
                _default_date("2001-01-01"),
                "2000-01-01"
            )
        self.assertEqual(context.exception.args[0], "end_date must be of type datetime.datetime")

        with self.assertRaises(Exception) as context:
            generate_date_range(
                _default_date("2001-01-01"),
                "2000-01-01"
            )
        self.assertEqual(context.exception.args[0], "end_date must be of type datetime.datetime")

        with self.assertRaises(Exception) as context:
            generate_date_range(
                _default_date("2001-01-01"),
                "2000-01-01"
            )
        self.assertEqual(context.exception.args[0], "end_date must be of type datetime.datetime")

        self.assertListEqual(
            generate_date_range(start_date=_default_date("2000-01-01"), end_date=_default_date("2003-01-01"), freq_input="A", arrears=True),
            ["2001-01-01","2002-01-01","2003-01-01"]
        )

        self.assertListEqual(
            generate_date_range(start_date=_default_date("2000-01-01"), end_date=_default_date("2003-01-01"), freq_input="A", arrears=False),
            ["2000-01-01","2001-01-01", "2002-01-01"]
        )

        self.assertListEqual(
            generate_date_range(start_date=_default_date("2000-01-01"), end_date=_default_date("2000-04-01"), freq_input="M", arrears=False),
            ["2000-01-01","2000-02-01","2000-03-01"]
        )

        self.assertListEqual(
            generate_date_range(start_date=_default_date("2000-01-01"), end_date=_default_date("2000-04-01"), freq_input="M", arrears=True),
            ["2000-02-01","2000-03-01","2000-04-01"]
        )

    def test_annual_range(self):

        with self.assertRaises(Exception) as context:
            _annual_range(
                _default_date("2001-01-01"),
                _default_date("2000-01-01")
            )
        self.assertEqual(context.exception.args[0], "start_date is after end_date")

        with self.assertRaises(Exception) as context:
            _annual_range(
                "2000-01-01",
                _default_date("2001-01-01")
            )
        self.assertEqual(context.exception.args[0], "start_date must be of type datetime.datetime")

        with self.assertRaises(Exception) as context:
            _annual_range(
                _default_date("2001-01-01"),
                "2000-01-01"
            )
        self.assertEqual(context.exception.args[0], "end_date must be of type datetime.datetime")

        pd.testing.assert_index_equal(
            _annual_range(_default_date("2000-01-01"), _default_date("2000-01-01")),
            pd.DatetimeIndex(["2000-01-01"])
        )

        pd.testing.assert_index_equal(
            _annual_range(_default_date("2000-01-01"), _default_date("2000-01-01")),
            pd.DatetimeIndex(["2000-01-01"])
        )

        pd.testing.assert_index_equal(
            _annual_range(_default_date("2000-01-01"), _default_date("2003-01-01")),
            pd.DatetimeIndex(["2000-01-01", "2001-01-01", "2002-01-01", "2003-01-01"])
        )

    def test_monthly_range(self):

        with self.assertRaises(Exception) as context:
            _monthly_range(
                _default_date("2001-01-01"),
                _default_date("2000-01-01")
            )
        self.assertEqual(context.exception.args[0], "start_date is after end_date")

        with self.assertRaises(Exception) as context:
            _monthly_range(
                "2000-01-01",
                _default_date("2001-01-01")
            )
        self.assertEqual(context.exception.args[0], "start_date must be of type datetime.datetime")

        with self.assertRaises(Exception) as context:
            _monthly_range(
                _default_date("2001-01-01"),
                "2000-01-01"
            )
        self.assertEqual(context.exception.args[0], "end_date must be of type datetime.datetime")

        pd.testing.assert_index_equal(
            _monthly_range(_default_date("2000-01-01"), _default_date("2000-03-01")).strftime("%Y-%m-%d"), 
            pd.DatetimeIndex(["2000-01-01", "2000-02-01", "2000-03-01"]).strftime("%Y-%m-%d")
        )

        pd.testing.assert_index_equal(
            _monthly_range(_default_date("2000-01-10"), _default_date("2000-03-10")).strftime("%Y-%m-%d"), 
            pd.DatetimeIndex(["2000-01-10", "2000-02-10", "2000-03-10"]).strftime("%Y-%m-%d")
        )

    def test_mid_month_adj(self):

        with self.assertRaises(Exception) as context:
            _mid_month_adj(
                _default_date("2000-01-01"),
                None
            )
        self.assertEqual(context.exception.args[0], "'None' is not of type pd.DatetimeIndex.")

        with self.assertRaises(Exception) as context:
            _mid_month_adj(
                "2000-01-01",
                pd.date_range("2000-01-01", "2001-01-01")
            )
        self.assertEqual(context.exception.args[0], "'2000-01-01' is not of type datetime.datetime.")

        self.assertCountEqual(
            _mid_month_adj(_default_date("2000-01-20"), pd.date_range("2000-01-01", "2000-03-01", freq="MS")).strftime("%Y-%m-%d"),
            pd.DatetimeIndex(["2000-01-20", "2000-02-20", "2000-03-20"]).strftime("%Y-%m-%d")
        )

        self.assertCountEqual(
            _mid_month_adj(_default_date("2000-01-01"), pd.date_range("2000-01-01", "2000-03-01", freq="MS")).strftime("%Y-%m-%d"),
            pd.DatetimeIndex(["2000-01-01", "2000-02-01", "2000-03-01"]).strftime("%Y-%m-%d")
        )

    def test_pd_generate_date_range(self):

        pd.testing.assert_index_equal(
            _generate_pd_date_range(_default_date("2000-01-01"), _default_date("2000-03-01"), 'MS'),
            pd.DatetimeIndex(["2000-01-01", "2000-02-01", "2000-03-01"], dtype='datetime64[ns]', freq=None)
        )

        pd.testing.assert_index_equal(
            _generate_pd_date_range(_default_date("2000-01-10") - pd.offsets.MonthBegin(), _default_date("2000-03-10"), 'MS'),
            pd.DatetimeIndex(["2000-01-01", "2000-02-01", "2000-03-01"], dtype='datetime64[ns]', freq=None)
        )

    def test_get_n_monthly(self):

        # Empty
        with self.assertRaises(Exception) as context:
            _get_n_monthly([], "A")
        # Non datetime.datetime
        with self.assertRaises(Exception) as context:
            _get_n_monthly(["2000-01-01"], "A")

        # Semi-Annual
        self.assertEqual(
            _get_n_monthly(
                [
                    datetime.strptime("2000-01-01", "%Y-%m-%d"), 
                    datetime.strptime("2000-02-01", "%Y-%m-%d"),
                    datetime.strptime("2000-03-01", "%Y-%m-%d"),
                    datetime.strptime("2000-04-01", "%Y-%m-%d"),
                    datetime.strptime("2000-05-01", "%Y-%m-%d"),
                    datetime.strptime("2000-06-01", "%Y-%m-%d"),
                    datetime.strptime("2000-07-01", "%Y-%m-%d"),
                    datetime.strptime("2000-08-01", "%Y-%m-%d"),
                    datetime.strptime("2000-09-01", "%Y-%m-%d"),
                    datetime.strptime("2000-10-01", "%Y-%m-%d"),
                    datetime.strptime("2000-11-01", "%Y-%m-%d"),
                    datetime.strptime("2000-12-01", "%Y-%m-%d"),
                    datetime.strptime("2001-01-01", "%Y-%m-%d")
                ],
                "SA"
            ),
            [
                datetime.strptime("2000-01-01", "%Y-%m-%d"),
                datetime.strptime("2000-07-01", "%Y-%m-%d"),
                datetime.strptime("2001-01-01", "%Y-%m-%d")
            ]
        )
        # Quarterly
        self.assertEqual(
            _get_n_monthly(
                [
                    datetime.strptime("2000-01-01", "%Y-%m-%d"), 
                    datetime.strptime("2000-02-01", "%Y-%m-%d"),
                    datetime.strptime("2000-03-01", "%Y-%m-%d"),
                    datetime.strptime("2000-04-01", "%Y-%m-%d"),
                    datetime.strptime("2000-05-01", "%Y-%m-%d"),
                    datetime.strptime("2000-06-01", "%Y-%m-%d"),
                    datetime.strptime("2000-07-01", "%Y-%m-%d"),
                    datetime.strptime("2000-08-01", "%Y-%m-%d"),
                    datetime.strptime("2000-09-01", "%Y-%m-%d"),
                    datetime.strptime("2000-10-01", "%Y-%m-%d"),
                    datetime.strptime("2000-11-01", "%Y-%m-%d"),
                    datetime.strptime("2000-12-01", "%Y-%m-%d"),
                    datetime.strptime("2001-01-01", "%Y-%m-%d")
                ],
                "Q"
            ),
            [
                datetime.strptime("2000-01-01", "%Y-%m-%d"), 
                datetime.strptime("2000-04-01", "%Y-%m-%d"),
                datetime.strptime("2000-07-01", "%Y-%m-%d"),
                datetime.strptime("2000-10-01", "%Y-%m-%d"),
                datetime.strptime("2001-01-01", "%Y-%m-%d")
            ]
        )
        # Monthly
        self.assertEqual(
            _get_n_monthly(
                [
                    datetime.strptime("2000-01-01", "%Y-%m-%d"), 
                    datetime.strptime("2000-02-01", "%Y-%m-%d"),
                    datetime.strptime("2000-03-01", "%Y-%m-%d"),
                    datetime.strptime("2000-04-01", "%Y-%m-%d"),
                    datetime.strptime("2000-05-01", "%Y-%m-%d"),
                    datetime.strptime("2000-06-01", "%Y-%m-%d"),
                    datetime.strptime("2000-07-01", "%Y-%m-%d"),
                    datetime.strptime("2000-08-01", "%Y-%m-%d"),
                    datetime.strptime("2000-09-01", "%Y-%m-%d"),
                    datetime.strptime("2000-10-01", "%Y-%m-%d"),
                    datetime.strptime("2000-11-01", "%Y-%m-%d"),
                    datetime.strptime("2000-12-01", "%Y-%m-%d"),
                    datetime.strptime("2001-01-01", "%Y-%m-%d")
                ],
                "M"
            ),
            [
                datetime.strptime("2000-01-01", "%Y-%m-%d"), 
                datetime.strptime("2000-02-01", "%Y-%m-%d"),
                datetime.strptime("2000-03-01", "%Y-%m-%d"),
                datetime.strptime("2000-04-01", "%Y-%m-%d"),
                datetime.strptime("2000-05-01", "%Y-%m-%d"),
                datetime.strptime("2000-06-01", "%Y-%m-%d"),
                datetime.strptime("2000-07-01", "%Y-%m-%d"),
                datetime.strptime("2000-08-01", "%Y-%m-%d"),
                datetime.strptime("2000-09-01", "%Y-%m-%d"),
                datetime.strptime("2000-10-01", "%Y-%m-%d"),
                datetime.strptime("2000-11-01", "%Y-%m-%d"),
                datetime.strptime("2000-12-01", "%Y-%m-%d"),
                datetime.strptime("2001-01-01", "%Y-%m-%d")
            ]
        )

    def test_default_date(self):

        # Pre-checks
        ## Is string
        with self.assertRaises(Exception) as context:
            _default_date(12)
        ## Throws exception when string format not correct
        with self.assertRaises(Exception) as context:
            _default_date("01-01-2000")
        
        self.assertEqual(_default_date("2000-01-01"), datetime.strptime("2000-01-01", "%Y-%m-%d"), "Normal case failed.")
