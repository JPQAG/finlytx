import unittest

from analytics.yield_return import YieldReturn


class TestYieldReturn(unittest.TestCase):
    def test_discounted_cash_flow(self):
        returnValue = YieldReturn.discounted_cash_flow("input string")

        assert type(returnValue) is dict

    # TODO
    # Get yield from current value, future value and cashflows.
    # Get
