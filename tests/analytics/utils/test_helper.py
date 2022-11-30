import unittest
import datetime

from src.analytics.utils.helper import (
    calculate_years_between_dates,
    convert_date_series_to_years,
    get_dict_from_list
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
    
    # Test empty dict
    def test_list_empty_raises(self):
        
        dict_list = []
        
        with self.assertRaises(Exception) as context:
            get_dict_from_list(dict_list, "key", "value")
        self.assertEqual(context.exception.args[0], "List must not be empty.")
    
    
    # Test key is string
    def test_key_type_is_string(self):
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
        
        with self.assertRaises(Exception) as context:
            get_dict_from_list(dict_list, 2, "value")
        self.assertEqual(context.exception.args[0], "Key must be of type string.")
    
    #Test dictionaries contain same keys
    def test_dicts_different_keys_throws(self):
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
                "NonMatchingKey": "valThreeThree"
            }
        ]
        
        with self.assertRaises(Exception) as context:
            get_dict_from_list(dict_list, "keyOne", "valOneOne")
        self.assertEqual(context.exception.args[0], "Keys of dictionaries must match.")
    
    #Test key in keys
    def test_raises_when_key_not_in_dicts(self):
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
        
        with self.assertRaises(Exception) as context:
            get_dict_from_list(dict_list, "NonExistantKey", "valOneOne")
        self.assertEqual(context.exception.args[0], "Key not found in dicts.")
    
    # Match not found
    def test_get_dict_from_list_no_match_val(self):
        
        dict_list = [
            {
                "keyOne": "valOneOne",
                "keyTwo": "valOneTwo",
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
        
        with self.assertRaises(Exception) as context:
            get_dict_from_list(dict_list, "keyOne", "NonExistantValue")
        self.assertEqual(context.exception.args[0], "Key/Val not found in provided list.")
        
    def test_get_dict_from_list_empty_dicts(self):
        dict_list = [{},{},{}]
        
        with self.assertRaises(Exception) as context:
            get_dict_from_list(dict_list, "", "")
        self.assertRaises(Exception)
    
    def test_get_dict_from_list(self):
        
        dict_list = [
            {
                "keyOne": "valOneOne",
                "keyTwo": "valOneTwo",
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
        
        result = get_dict_from_list(dict_list, "keyTwo", "valOneTwo")
        
        expected = {
            "keyOne": "valOneOne",
            "keyTwo": "valOneTwo",
            "keyThree": "valOneThree"
        }
        
        self.assertEqual(result, expected)
        
        
        
        
        
        