import unittest
import datetime
import numpy as np

from analytics.utils.curve import (
    construct_ns_curve,
    construct_nss_curve,
    convert_curve_dict_list_to_lists
)


from ..helper.testConstants import (
    MOCK_BENCHMARK_CURVE,
    MOCK_BENCHMARK_CURVE_AS_YEARS, 
    MOCK_BENCHMARK_CURVE_AS_YEARS_AS_LISTS
)

from analytics.utils.regression.calibrate import calibrate_ns_ols
from analytics.utils.regression.calibrate import calibrate_nss_ols

class SecurityAnalysisTestCase(unittest.TestCase):
    def test_construct_ns_curve(self):

        market_curve = MOCK_BENCHMARK_CURVE

        result = construct_ns_curve(
            datetime.datetime(1999, 1, 1),
            market_curve
        )

        expected, opt = calibrate_ns_ols(
            np.array(MOCK_BENCHMARK_CURVE_AS_YEARS_AS_LISTS[0]),
            np.array(MOCK_BENCHMARK_CURVE_AS_YEARS_AS_LISTS[1]),
            tau0=1.0
        )

        self.assertEqual(result, expected)

    def test_construct_nss_curve(self):

        market_curve = MOCK_BENCHMARK_CURVE

        result = construct_nss_curve(
            datetime.datetime(1999, 1, 1),
            market_curve
        )

        expected, opt = calibrate_nss_ols(
            np.array(MOCK_BENCHMARK_CURVE_AS_YEARS_AS_LISTS[0]),
            np.array(MOCK_BENCHMARK_CURVE_AS_YEARS_AS_LISTS[1]),
            tau0 = np.array([2.2, 3.1])
        )

        self.assertEqual(result, expected)

    def test_convert_curve_dict_list_to_list(self):

        result = convert_curve_dict_list_to_lists(MOCK_BENCHMARK_CURVE_AS_YEARS)

        self.assertEqual(result, MOCK_BENCHMARK_CURVE_AS_YEARS_AS_LISTS)


