import unittest

from analytics.yield_return import YieldReturn


class TestYieldReturn(unittest.TestCase):
    def test_yield_to_workout(self):
        returnValue = YieldReturn.yield_to_workout(self)

        assert isinstance(returnValue, float) is True

        

