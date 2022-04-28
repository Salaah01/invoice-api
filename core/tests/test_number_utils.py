"""Unit tests for the number utils."""

import unittest
from decimal import Decimal
from .. import number_utils as utils


class TestFloatToDp(unittest.TestCase):
    """Unittests for the `float_to_dp` function."""

    def test_round_down(self):
        """Test that the decimal is rounded down."""
        self.assertEqual(utils.float_to_dp(1.234999, 2), 1.23)

    def test_round_up(self):
        """Test that the decimal is rounded up."""
        self.assertEqual(utils.float_to_dp(1.235, 2), 1.24)

    def test_as_decimal(self):
        """Test that the decimal is returned as a decimal."""
        result = utils.float_to_dp(1.26, 2, as_decimal=True)
        self.assertIsInstance(result, Decimal)
        self.assertEqual(result, Decimal("1.26"))
