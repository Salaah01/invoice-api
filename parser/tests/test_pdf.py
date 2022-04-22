"""Unittests for the `pdf` module."""

import unittest
from .. import pdf


class TestParser(unittest.TestCase):
    """Unittests for the `parser` function."""

    def test_parses_data(self):
        """Test that the function is able to correctly parse a pdf."""
        result = pdf.parser("parser/tests/test_pdf.pdf")
        self.assertEqual(
            result,
            ["Page 1", "paragraph 1", "page 2", "paragraph 2"],
        )
