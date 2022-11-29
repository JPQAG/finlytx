import unittest
import datetime
import numpy as np

from src.analytics.utils.regression.ns import NelsonSiegelCurve
from src.analytics.utils.regression.nss import NelsonSiegelSvenssonCurve

from src.analytics.utils.curve import (
    bootstrap_curve,
    construct_ns_curve,
    ns_curve_output,
    construct_nss_curve,
    nss_curve_output,
    convert_curve_dict_list_to_lists,
    forward_curve,
    curve_set,
    _clean_curve_tenor_round
)

from ..helper.testConstants import (
    MOCK_BENCHMARK_CURVE,
    MOCK_BENCHMARK_CURVE_AS_YEARS, 
    MOCK_BENCHMARK_CURVE_AS_YEARS_AS_LISTS,
    MOCK_BENCHMARK_CURVE_CLEAN_TENOR
)

from src.analytics.utils.regression.calibrate import calibrate_ns_ols, calibrate_nss_ols

class CurveTestCase(unittest.TestCase):
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

    def test_ns_curve_output(self):
        market_curve = MOCK_BENCHMARK_CURVE

        result = construct_ns_curve(
            datetime.datetime(1999, 1, 1),
            market_curve
        )
        
        result = ns_curve_output(result, np.linspace(0, 30, num=30*12).tolist())
        
        self.assertEqual(result[12], {'tenor': 1.0027855153203342, 'rate': -0.006983785586190569})

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

    def test_nss_curve_output(self):
        market_curve = MOCK_BENCHMARK_CURVE

        result = construct_nss_curve(
            datetime.datetime(1999, 1, 1),
            market_curve
        )
        
        result = nss_curve_output(result, np.linspace(0, 30, num=30*12).tolist())
        
        self.assertEqual(result[12], {'tenor': 1.0027855153203342, 'rate': 0.004595117271485261})

    def test_convert_curve_dict_list_to_list(self):

        result = convert_curve_dict_list_to_lists(MOCK_BENCHMARK_CURVE_AS_YEARS)

        self.assertEqual(result, MOCK_BENCHMARK_CURVE_AS_YEARS_AS_LISTS)

class BootstrapCurveTestCase(unittest.TestCase):

    def test_boostrap_curve(self):
        """CFA LEVEL 2 - CFA 2018.
        Fixed Income - Spot Rates and Forward Rates. Constructing the zero curve from market/spot/par.
        """

        curve = [
            {
                "tenor": 1.0,
                "rate": 0.05
            },
            {
                "tenor": 2.0,
                "rate": 0.0597
            },
            {
                "tenor": 3.0,
                "rate": 0.0691
            },
            {
                "tenor": 4.00,
                "rate": 0.0781
            },
        ]

        expected = [
            {
                "tenor": 1.0,
                "rate": 0.05
            },
            {
                "tenor": 2.0,
                "rate": 0.06
            },
            {
                "tenor": 3.0,
                "rate": 0.07
            },
            {
                "tenor": 4.00,
                "rate": 0.08
            },
        ]

        result = bootstrap_curve(curve)

        self.assertEqual(result, expected)

    def test_bootstrap_empty_curve(self):
        curve = []

        with self.assertRaises(Exception) as context:
            bootstrap_curve(
                curve
            )
        self.assertEqual(context.exception.args[0], "Provided curve is empty!")

    def test_bootstrap_curve_wrong_type(self):
        curve = [
            {
                "tenor": 'string',
                "rate": 1.0
            }
        ]

        with self.assertRaises(Exception) as context:
            bootstrap_curve(
                curve
            )
        self.assertEqual(context.exception.args[0], "All curve tenors must be of type float!")

class ForwardCurveTestCase(unittest.TestCase):

    def test_forward_curve_empty_market_curve(self):
        market_curve = []
        
        with self.assertRaises(Exception) as context:
            forward_curve(
                market_curve,
                1
            )
        self.assertEqual(context.exception.args[0], "Curve input must not be an empty list.")
        
    def test_forward_curve_number_of_tenors_input(self):
        market_curve = [
            {
                "tenor": 1,
                "rate": 0.02548
            }
        ]
        
        with self.assertRaises(Exception) as context:
            forward_curve(
                market_curve,
                1
            )
        self.assertEqual(context.exception.args[0], "Curve input must contain more than one object!")
        
    def test_forward_curve_object_contents_type_tenors(self):
        market_curve = [
            {
                "tenor": 1,
                "rate": 0.02548
            },
            {
                "tenor": "2",
                "rate": 0.02983
            },
            {
                "tenor": 3,
                "rate": 0.02891
            }
        ]
        
        with self.assertRaises(Exception) as context:
            forward_curve(
                market_curve,
                1
            )
        self.assertEqual(context.exception.args[0], "Tenors must be of type float.")
        
    def test_forward_curve_object_contents_type_rates(self):
        market_curve = [
            {
                "tenor": 1.00,
                "rate": 0.02548
            },
            {
                "tenor": 2.00,
                "rate": "0.02983"
            },
            {
                "tenor": 3.00,
                "rate": 0.02891
            }
        ]
        
        with self.assertRaises(Exception) as context:
            forward_curve(
                market_curve,
                1
            )
        self.assertEqual(context.exception.args[0], "Rates must be of type float.")

    def test_forward_curve(self):

        expected = [
            {
                "settle_tenor": 1.0,
                "workout_tenor": 2.0,
                "rate": 0.03420
            },
            {
                "settle_tenor": 2.0,
                "workout_tenor": 3.0,
                "rate": 0.02707
            }
        ]

        market_curve = [
            {
                "tenor": 1.00,
                "rate": 0.02548
            },
            {
                "tenor": 2.00,
                "rate": 0.02983
            },
            {
                "tenor": 3.00,
                "rate": 0.02891
            }
        ]

        result = forward_curve(
            market_curve,
            1
        )

        self.assertEqual(result, expected)

class CurveSetTestCase(unittest.TestCase):
    
    def test_curve_set_empty_curve(self):
        market_curve = MOCK_BENCHMARK_CURVE

        result = curve_set(
            datetime.datetime(1999, 1, 1),
            market_curve,
            ["Q", "SA"]
        )
    
    def test_curve_set_not_enough_data(self):
        pass
    
class CleanCurveTestCase(unittest.TestCase):
    
    def test_clean_curve_tenor_round(self):
    
        market_curve = MOCK_BENCHMARK_CURVE
        
        constructed_curve = construct_ns_curve(datetime.datetime(1999, 1, 1), market_curve)
        interpolated_market_curve = ns_curve_output(constructed_curve, np.linspace(0, 10, num=5).tolist())
        
        result = _clean_curve_tenor_round(interpolated_market_curve, 2)
        
        expected = MOCK_BENCHMARK_CURVE_CLEAN_TENOR
        
        self.assertEqual(result, expected)