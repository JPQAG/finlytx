import unittest
import datetime

from src.analytics.utils.helper import (
    calculate_years_between_dates,
    convert_date_series_to_years
)
from ..helper.testConstants  import ( 
    MOCK_BENCHMARK_CURVE, 
    MOCK_BENCHMARK_CURVE_AS_LISTS,
    MOCK_BENCHMARK_CURVE_AS_YEARS
)

class HelperTestCase(unittest.TestCase):
    
    def test_calculate_years_between_dates(self):

        start_date = datetime.datetime(2000, 1, 1)
        end_date = datetime.datetime(2001, 1, 1)

        result = calculate_years_between_dates(
            start_date,
            end_date
        )

        self.assertEqual(result, 1)

    def test_convert_date_series_to_years(self):
        """Convert a list of dicts containing date attribute to
            have relative 'time' value instead of date.
        """

        series = MOCK_BENCHMARK_CURVE
        relative_date = datetime.datetime(1999, 1, 1)

        result = convert_date_series_to_years(series, relative_date)

        self.assertEqual(result, MOCK_BENCHMARK_CURVE_AS_YEARS)
        
class GetDictFromListTestCase(unittest.TestCase):
    
    def test_filter_DictList(self):
        
        dict_list = [
            {
                "keyOne": "valOneOne",
                "keyTwo": "valOneTwi",
                "keyThree": "valOneThree"
            },
            {
                "keyOne": "valTwoOne",
                "keyTwo": "valTwoTwo",
                "keyThree": "valTwoThree"
            },
            {
                "keyOne": "valThreeOne",
                "keyTwo": "valThreeTwo",
                "keyThree": "valThreeThree"
            }
        ]
        
        