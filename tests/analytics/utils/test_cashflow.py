import unittest
import datetime
from datetime import ( time )
import numpy as np
from finx.analytics.utils.cashflow import (
    generate_cashflows, 
    get_most_recent_cashflow,
    match_cashflow_to_discount_curve, 
    sum_cashflows, 
    trim_cashflows_after_workout,
    generate_cashflows,
    _get_variable_coupon_component
)
from finx.analytics.utils.lookup import TIMESERIES_TIME_PERIODS, CURVE_OPTIONS

from ..helper.testConstants import (
    MOCK_CASHFLOW_AND_DISCOUNT_CURVE, 
    MOCK_DISCOUNT_CURVE, 
    MOCK_SECURITY_CASHFLOW_ARRAY, 
    MOCK_SECURITY_FIXED_RATE_CASHFLOW_ARRAY,
    MOCK_NSS_CURVE_PARAMETERS,
    MOCK_NSS_CURVE_RESULT
)

from finx.analytics.utils.regression.ns import NelsonSiegelCurve
from finx.analytics.utils.regression.nss import NelsonSiegelSvenssonCurve

class CashflowTestCase(unittest.TestCase):
    def test_match_cashflow_to_discount_curve(self):

        cashflows = MOCK_SECURITY_CASHFLOW_ARRAY
        discount_curve = MOCK_DISCOUNT_CURVE

        result = match_cashflow_to_discount_curve(cashflows, discount_curve)

        self.assertEqual(result, MOCK_CASHFLOW_AND_DISCOUNT_CURVE)

    def test_sum_cashflows(self):

        result = sum_cashflows(MOCK_SECURITY_CASHFLOW_ARRAY)

        self.assertEqual(result, 18000)

    def test_trim_cashflows_after_workout(self):

        cashflows = MOCK_SECURITY_CASHFLOW_ARRAY
        workout_date = MOCK_SECURITY_CASHFLOW_ARRAY[-2]['date']

        result = trim_cashflows_after_workout(cashflows, workout_date)

        self.assertEqual(result, cashflows[0:-1])

    def test_get_most_recent_cashflow(self):

        # Between first and second cashflow
        self.assertEqual(get_most_recent_cashflow(datetime.datetime(2001,4,1), MOCK_SECURITY_CASHFLOW_ARRAY), MOCK_SECURITY_CASHFLOW_ARRAY[0])
        # Reference date equals second cashflow date
        self.assertEqual(get_most_recent_cashflow(datetime.datetime(2002,1,1), MOCK_SECURITY_CASHFLOW_ARRAY), MOCK_SECURITY_CASHFLOW_ARRAY[1])
        # Before first cashflow throws exception
        with self.assertRaises(ValueError):
            get_most_recent_cashflow(datetime.datetime(1999,1,1), MOCK_SECURITY_CASHFLOW_ARRAY)
        # Empty cashflow array
        with self.assertRaises(ValueError):
            get_most_recent_cashflow(datetime.datetime(2001,4,1), [])

class GenerateCashflowTestCase(unittest.TestCase):
        
    def test_generate_cashflows_args_error_start_date_type_incorrect(self):

        coupon_rate_periodic = 0.05/1

        with self.assertRaises(Exception) as context:
            generate_cashflows(
                start_date = "2000-01-01",
                end_date = datetime.datetime.strptime("2000-12-01", "%Y-%m-%d"),
                cashflow_freq = "M",
                face_value = 100,
                coupon_rate_or_margin= coupon_rate_periodic
            )
        self.assertEqual(context.exception.args[0], "Date arguments must be of type datetime.")

    def test_generate_cashflows_args_error_start_date_type_incorrect(self):

        coupon_rate_periodic = 0.05/1

        with self.assertRaises(Exception) as context:
            generate_cashflows(
                start_date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d"),
                end_date = "2000-12-01",
                cashflow_freq = "M",
                face_value = 100,
                coupon_rate_or_margin= coupon_rate_periodic
            )
        self.assertEqual(context.exception.args[0], "Date arguments must be of type datetime.")

    def test_generate_cashflows_args_error_freq(self):
        
        coupon_rate_periodic = 0.05/1

        with self.assertRaises(Exception) as context:
            generate_cashflows(
                start_date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d"),
                end_date = datetime.datetime.strptime("2000-12-01", "%Y-%m-%d"),
                cashflow_freq = "PSQ",
                face_value = 100,
                coupon_rate_or_margin= coupon_rate_periodic
            )
        self.assertEqual(context.exception.args[0], f"'PSQ' is not in {TIMESERIES_TIME_PERIODS.keys()}.")

    def test_generate_cashflows_args_error_float_type(self):
        
        coupon_rate_periodic = 0.05/1
        
        with self.assertRaises(Exception) as context:
            generate_cashflows(
                start_date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d"),
                end_date = datetime.datetime.strptime("2000-12-01", "%Y-%m-%d"),
                cashflow_freq = "M",
                face_value = "String incorrect type",
                coupon_rate_or_margin= coupon_rate_periodic
            )
        self.assertEqual(context.exception.args[0], "Numeric args must be of float type.")

    def test_generate_monthly_fixed_cashflows(self):

        coupon_rate_periodic = 0.05/12
        ex_record_config = {
            "record_date": {
                "days_before_payment_date": 8,
                "record_time": 19,
                "day_type": "calendar",
                "time_of_record": time(hour=19)
            }
        }

        expected = [
            {
                'date': {
                    "payment_date": "2000-02-01",
                    "record_date": "2000-01-24",
                    "ex_date": "2000-01-23"
                },
                'cashflow': {
                    'total': coupon_rate_periodic * 100,
                    'coupon_interest': {
                        'fixed_coupon_interest_component': coupon_rate_periodic * 100,
                        'variable_coupon_interest_component': 0,
                        'total_coupon_interest': coupon_rate_periodic * 100,
                    },
                    'principal': {
                        'redemption_principal': 0,
                        'amortising': 0,
                        'total_principal': 0
                    }
                }
            },
            {
                'date': {
                    "payment_date": "2000-03-01",
                    "record_date": "2000-02-22",
                    "ex_date": "2000-02-21"
                },
                'cashflow': {
                    'total': coupon_rate_periodic * 100,
                    'coupon_interest': {
                        'fixed_coupon_interest_component': coupon_rate_periodic * 100,
                        'variable_coupon_interest_component': 0,
                        'total_coupon_interest': coupon_rate_periodic * 100,
                    },
                    'principal': {
                        'redemption_principal': 0,
                        'amortising': 0,
                        'total_principal': 0
                    }
                }
            },
            {
                'date': {
                    "payment_date": "2000-04-01",
                    "record_date": "2000-03-24",
                    "ex_date": "2000-03-23"
                },
                'cashflow': {
                    'total': coupon_rate_periodic * 100,
                    'coupon_interest': {
                        'fixed_coupon_interest_component': coupon_rate_periodic * 100,
                        'variable_coupon_interest_component': 0,
                        'total_coupon_interest': coupon_rate_periodic * 100,
                    },
                    'principal': {
                        'redemption_principal': 0,
                        'amortising': 0,
                        'total_principal': 0
                    }
                }
            },
            {
                'date': {
                    "payment_date": "2000-05-01",
                    "record_date": "2000-04-23",
                    "ex_date": "2000-04-22"
                },
                'cashflow': {
                    'total': coupon_rate_periodic * 100,
                    'coupon_interest': {
                        'fixed_coupon_interest_component': coupon_rate_periodic * 100,
                        'variable_coupon_interest_component': 0,
                        'total_coupon_interest': coupon_rate_periodic * 100,
                    },
                    'principal': {
                        'redemption_principal': 0,
                        'amortising': 0,
                        'total_principal': 0
                    }
                }
            },
            {
                'date': {
                    "payment_date": "2000-06-01",
                    "record_date": "2000-05-24",
                    "ex_date": "2000-05-23"
                },
                'cashflow': {
                    'total': coupon_rate_periodic * 100,
                    'coupon_interest': {
                        'fixed_coupon_interest_component': coupon_rate_periodic * 100,
                        'variable_coupon_interest_component': 0,
                        'total_coupon_interest': coupon_rate_periodic * 100,
                    },
                    'principal': {
                        'redemption_principal': 0,
                        'amortising': 0,
                        'total_principal': 0
                    }
                }
            },
            {
                'date': {
                    "payment_date": "2000-07-01",
                    "record_date": "2000-06-23",
                    "ex_date": "2000-06-22"
                },
                'cashflow': {
                    'total': coupon_rate_periodic * 100,
                    'coupon_interest': {
                        'fixed_coupon_interest_component': coupon_rate_periodic * 100,
                        'variable_coupon_interest_component': 0,
                        'total_coupon_interest': coupon_rate_periodic * 100,
                    },
                    'principal': {
                        'redemption_principal': 0,
                        'amortising': 0,
                        'total_principal': 0
                    }
                }
            },
            {
                'date': {
                    "payment_date": "2000-08-01",
                    "record_date": "2000-07-24",
                    "ex_date": "2000-07-23"
                },
                'cashflow': {
                    'total': coupon_rate_periodic * 100,
                    'coupon_interest': {
                        'fixed_coupon_interest_component': coupon_rate_periodic * 100,
                        'variable_coupon_interest_component': 0,
                        'total_coupon_interest': coupon_rate_periodic * 100,
                    },
                    'principal': {
                        'redemption_principal': 0,
                        'amortising': 0,
                        'total_principal': 0
                    }
                }
            },
            {
                'date': {
                    "payment_date": "2000-09-01",
                    "record_date": "2000-08-24",
                    "ex_date": "2000-08-23"
                },
                'cashflow': {
                    'total': coupon_rate_periodic * 100,
                    'coupon_interest': {
                        'fixed_coupon_interest_component': coupon_rate_periodic * 100,
                        'variable_coupon_interest_component': 0,
                        'total_coupon_interest': coupon_rate_periodic * 100,
                    },
                    'principal': {
                        'redemption_principal': 0,
                        'amortising': 0,
                        'total_principal': 0
                    }
                }
            },
            {
                'date': {
                    "payment_date": "2000-10-01",
                    "record_date": "2000-09-23",
                    "ex_date": "2000-09-22"
                },
                'cashflow': {
                    'total': coupon_rate_periodic * 100,
                    'coupon_interest': {
                        'fixed_coupon_interest_component': coupon_rate_periodic * 100,
                        'variable_coupon_interest_component': 0,
                        'total_coupon_interest': coupon_rate_periodic * 100,
                    },
                    'principal': {
                        'redemption_principal': 0,
                        'amortising': 0,
                        'total_principal': 0
                    }
                }
            },
            {
                'date': {
                    "payment_date": "2000-11-01",
                    "record_date": "2000-10-24",
                    "ex_date": "2000-10-23"
                },
                'cashflow': {
                    'total': coupon_rate_periodic * 100,
                    'coupon_interest': {
                        'fixed_coupon_interest_component': coupon_rate_periodic * 100,
                        'variable_coupon_interest_component': 0,
                        'total_coupon_interest': coupon_rate_periodic * 100,
                    },
                    'principal': {
                        'redemption_principal': 0,
                        'amortising': 0,
                        'total_principal': 0
                    }
                }
            },
            {
                'date': {
                    "payment_date": "2000-12-01",
                    "record_date": "2000-11-23",
                    "ex_date": "2000-11-22"
                },
                'cashflow': {
                    'total': coupon_rate_periodic * 100 + 100,
                    'coupon_interest': {
                        'fixed_coupon_interest_component': coupon_rate_periodic * 100,
                        'variable_coupon_interest_component': 0,
                        'total_coupon_interest': coupon_rate_periodic * 100,
                    },
                    'principal': {
                        'redemption_principal': 100,
                        'amortising': 0,
                        'total_principal': 100
                    }
                }
            }
        ]

        result = generate_cashflows(
            start_date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d"),
            end_date = datetime.datetime.strptime("2000-12-01", "%Y-%m-%d"),
            cashflow_freq = "M",
            face_value = 100.00,
            coupon_rate_or_margin= 0.05,
            ex_record_config=ex_record_config
        )

        self.assertEqual(result, expected)

    def test_generate_annual_fixed_cashflows(self):
        
        coupon_rate_periodic = 0.05/1
        
        ex_record_config = {
            "record_date": {
                "days_before_payment_date": 8,
                "record_time": 19,
                "day_type": "calendar",
                "time_of_record": time(hour=19)
            }
        }

        expected = [
            {
                'date': {
                    "payment_date": "2001-01-01",
                    "record_date": "2000-12-24",
                    "ex_date": "2000-12-23"
                },
                'cashflow': {
                    'total': coupon_rate_periodic * 100 + 100,
                    'coupon_interest': {
                        'fixed_coupon_interest_component': coupon_rate_periodic * 100,
                        'variable_coupon_interest_component': 0,
                        'total_coupon_interest': coupon_rate_periodic * 100,
                    },
                    'principal': {
                        'redemption_principal': 100,
                        'amortising': 0,
                        'total_principal': 100
                    }
                }
            }
        ]

        result = generate_cashflows(
            start_date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d"),
            end_date = datetime.datetime.strptime("2001-01-01", "%Y-%m-%d"),
            cashflow_freq = "A",
            face_value = 100.00,
            coupon_rate_or_margin= 0.05,
            ex_record_config=ex_record_config
        )

        self.assertEqual(result, expected)

    def test_generate_annual_floating_cashflows(self):
        
        coupon_margin_periodic = 0.03/1
        
        ex_record_config = {
            "record_date": {
                "days_before_payment_date": 8,
                "record_time": 19,
                "day_type": "calendar",
                "time_of_record": time(hour=19)
            }
        }

        expected = [
            {
                'date': {
                    "payment_date": "2001-01-01",
                    "record_date": "2000-12-24",
                    "ex_date": "2000-12-23"
                },
                'cashflow': {
                    'total': round((coupon_margin_periodic * 100) + 100 + MOCK_NSS_CURVE_RESULT[0], 4),
                    'coupon_interest': {
                        'fixed_coupon_interest_component': coupon_margin_periodic * 100,
                        'variable_coupon_interest_component': MOCK_NSS_CURVE_RESULT[0],
                        'total_coupon_interest': coupon_margin_periodic * 100,
                    },
                    'principal': {
                        'redemption_principal': 100,
                        'amortising': 0,
                        'total_principal': 100
                    }
                },
            }
        ]
        expected_dates = [dictionary['date'] for dictionary in expected]
        expected_total_cashflows = [dictionary['cashflow']['total'] for dictionary in expected]
        expected_total_fixed_cashflows = [
            dictionary['cashflow']['coupon_interest']['fixed_coupon_interest_component']
            for
            dictionary in expected
        ]
        expected_total_variable_cashflows = [
            dictionary['cashflow']['coupon_interest']['variable_coupon_interest_component']
            for
            dictionary in expected
        ]
        
        nss_params = MOCK_NSS_CURVE_PARAMETERS

        result = generate_cashflows(
            start_date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d"),
            end_date = datetime.datetime.strptime("2001-01-01", "%Y-%m-%d"),
            cashflow_freq = "A",
            face_value = 100.00,
            coupon_rate_or_margin = coupon_margin_periodic,
            variable_coupon=True,
            underlying_curve = NelsonSiegelSvenssonCurve(
                nss_params[0], 
                nss_params[1], 
                nss_params[2], 
                nss_params[3],
                nss_params[4],
                nss_params[5]
            ),
            pricing_date=datetime.datetime.strptime("2000-01-01", "%Y-%m-%d"),
            ex_record_config=ex_record_config
        )
        result_dates = [dictionary['date'] for dictionary in result]
        result_total_cashflows = [round(dictionary['cashflow']['total'], 4) for dictionary in result]
        result_total_fixed_cashflows = [
            round(dictionary['cashflow']['coupon_interest']['fixed_coupon_interest_component'], 4)
            for
            dictionary in result
        ]
        result_total_variable_cashflows = [
            round(dictionary['cashflow']['coupon_interest']['variable_coupon_interest_component'], 4)
            for
            dictionary in result
        ]
        
        self.assertTrue(np.allclose(result_total_cashflows, expected_total_cashflows, atol=1e-03))
        self.assertTrue(np.allclose(result_total_fixed_cashflows, expected_total_fixed_cashflows, atol=1e-03))
        self.assertTrue(np.allclose(result_total_variable_cashflows, expected_total_variable_cashflows, atol=1e-03))
        self.assertEqual(result_dates, expected_dates)
        
    def test_generate_annual_floating_cashflows_2Y(self):
        
        coupon_margin_periodic = 0.03/1
        ex_record_config = {
            "record_date": {
                "days_before_payment_date": 8,
                "record_time": 19,
                "day_type": "calendar",
                "time_of_record": time(hour=19)
            }
        }

        expected = [
            {
                'date': {
                    "payment_date": "2001-01-01",
                    "record_date": "2000-12-24",
                    "ex_date": "2000-12-23"
                },
                'cashflow': {
                    'total': round((coupon_margin_periodic * 100) + MOCK_NSS_CURVE_RESULT[0], 4),
                    'coupon_interest': {
                        'fixed_coupon_interest_component': coupon_margin_periodic * 100,
                        'variable_coupon_interest_component': MOCK_NSS_CURVE_RESULT[0],
                        'total_coupon_interest': coupon_margin_periodic * 100,
                    },
                    'principal': {
                        'redemption_principal': 0,
                        'amortising': 0,
                        'total_principal': 0
                    }
                },
            },
            {
                'date': {
                    "payment_date": "2002-01-01",
                    "record_date": "2001-12-24",
                    "ex_date": "2001-12-23"
                },
                'cashflow': round((coupon_margin_periodic * 100) + 100 + MOCK_NSS_CURVE_RESULT[1], 4),
                'cashflow': {
                    'total': round((coupon_margin_periodic * 100) + 100 + MOCK_NSS_CURVE_RESULT[1], 4),
                    'coupon_interest': {
                        'fixed_coupon_interest_component': coupon_margin_periodic * 100,
                        'variable_coupon_interest_component': MOCK_NSS_CURVE_RESULT[1],
                        'total_coupon_interest': coupon_margin_periodic * 100,
                    },
                    'principal': {
                        'redemption_principal': 100,
                        'amortising': 0,
                        'total_principal': 100
                    }
                }
            }
        ]
        expected_dates = [dictionary['date'] for dictionary in expected]
        expected_total_cashflows = [dictionary['cashflow']['total'] for dictionary in expected]
        expected_total_fixed_cashflows = [
            dictionary['cashflow']['coupon_interest']['fixed_coupon_interest_component']
            for
            dictionary in expected
        ]
        expected_total_variable_cashflows = [
            dictionary['cashflow']['coupon_interest']['variable_coupon_interest_component']
            for
            dictionary in expected
        ]
        
        nss_params = MOCK_NSS_CURVE_PARAMETERS

        result = generate_cashflows(
            start_date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d"),
            end_date = datetime.datetime.strptime("2002-01-01", "%Y-%m-%d"),
            cashflow_freq = "A",
            face_value = 100.00,
            coupon_rate_or_margin = coupon_margin_periodic,
            variable_coupon=True,
            underlying_curve = NelsonSiegelSvenssonCurve(
                nss_params[0], 
                nss_params[1], 
                nss_params[2], 
                nss_params[3],
                nss_params[4],
                nss_params[5]
            ),
            pricing_date=datetime.datetime.strptime("2000-01-01", "%Y-%m-%d"),
            ex_record_config=ex_record_config
        )
        result_dates = [dictionary['date'] for dictionary in result]
        result_total_cashflows = [round(dictionary['cashflow']['total'], 4) for dictionary in result]
        result_total_fixed_cashflows = [
            round(dictionary['cashflow']['coupon_interest']['fixed_coupon_interest_component'], 4)
            for
            dictionary in result
        ]
        result_total_variable_cashflows = [
            round(dictionary['cashflow']['coupon_interest']['variable_coupon_interest_component'], 4)
            for
            dictionary in result
        ]
        
        self.assertTrue(np.allclose(result_total_cashflows, expected_total_cashflows, atol=1e-03))
        self.assertTrue(np.allclose(result_total_fixed_cashflows, expected_total_fixed_cashflows, atol=1e-03))
        self.assertTrue(np.allclose(result_total_variable_cashflows, expected_total_variable_cashflows, atol=1e-03))
        self.assertEqual(result_dates, expected_dates)
    
class GenerateVariableCouponComponent(unittest.TestCase):
    
    def test_get_variable_coupon_component_input_type_pricing_date(self):
        
        pricing_date = "2000-01-01"
        coupon_payment_date = datetime.datetime.strptime("2004-01-01", "%Y-%m-%d")
        curve = NelsonSiegelCurve(0.017, -0.023, 0.24, 2.2)
        
        with self.assertRaises(Exception) as context:
            _get_variable_coupon_component(
                pricing_date,
                coupon_payment_date,
                curve
            )
        self.assertEqual(context.exception.args[0], "pricing_date must be of type datetime.datetime.")
        
    
    def test_get_variable_coupon_component_input_type_workout_date(self):
        
        pricing_date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d")
        coupon_payment_date = "2004-01-01"
        curve = NelsonSiegelCurve(0.017, -0.023, 0.24, 2.2)
        
        with self.assertRaises(Exception) as context:
            _get_variable_coupon_component(
                pricing_date,
                coupon_payment_date,
                curve
            )
        self.assertEqual(context.exception.args[0], "workout_date must be of type datetime.datetime.")
        
        
    def test_get_variable_coupon_component_input_type_curve(self):
        
        pricing_date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d")
        coupon_payment_date = datetime.datetime.strptime("2004-01-01", "%Y-%m-%d")
        curve = str(0.017)
        
        with self.assertRaises(Exception) as context:
            _get_variable_coupon_component(
                pricing_date,
                coupon_payment_date,
                curve
            )
        self.assertEqual(context.exception.args[0], f"underlying_forward_curve must be one of {CURVE_OPTIONS} as objects.")
        
    
    def test_get_variable_coupon_component(self):
        
        pricing_date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d")
        coupon_payment_date = datetime.datetime.strptime("2004-01-01", "%Y-%m-%d")
        curve = NelsonSiegelCurve(0.017, -0.023, 0.24, 2.2)
        
        expected = 0.07802
        
        result = _get_variable_coupon_component(
            pricing_date,
            coupon_payment_date,
            curve
        )
        
        self.assertEqual(round(result, 5), round(expected/100, 5))
        
    def test_get_variable_coupon_component_nss(self):
        
                
        pricing_date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d")
        coupon_payment_date = datetime.datetime.strptime("2001-01-01", "%Y-%m-%d")
        
        nss_params = MOCK_NSS_CURVE_PARAMETERS
        
        curve = NelsonSiegelSvenssonCurve(
            nss_params[0], 
            nss_params[1], 
            nss_params[2], 
            nss_params[3],
            nss_params[4],
            nss_params[5]
        )
        
        expected = MOCK_NSS_CURVE_RESULT[0]
        
        result = _get_variable_coupon_component(
            pricing_date,
            coupon_payment_date,
            curve
        )
        
        self.assertAlmostEqual(result, expected/100, 5)
        
    def test_get_variable_coupon_component_nss_two(self):
        
                
        pricing_date = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d")
        coupon_payment_date = datetime.datetime.strptime("2002-01-01", "%Y-%m-%d")
        
        nss_params = MOCK_NSS_CURVE_PARAMETERS
        
        curve = NelsonSiegelSvenssonCurve(
            nss_params[0], 
            nss_params[1], 
            nss_params[2], 
            nss_params[3],
            nss_params[4],
            nss_params[5]
        )
        
        expected = MOCK_NSS_CURVE_RESULT[1]
        
        result = _get_variable_coupon_component(
            pricing_date,
            coupon_payment_date,
            curve
        )
        
        self.assertAlmostEqual(result, expected/100, 5)
        
