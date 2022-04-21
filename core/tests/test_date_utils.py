from datetime import datetime, date
from django.test import SimpleTestCase
from core import date_utils


class TestDateToStr(SimpleTestCase):
    """Unittests for the `date_to_str` function."""

    def test_date_to_str(self):
        """Test that the function works as expected for a `date` object."""
        self.assertEqual(
            date_utils.date_to_str(date(2020, 2, 1)),
            '01/02/2020'
        )

    def test_datetime_to_str(self):
        """Test that the function works as expected for a `datetime` object."""
        self.assertEqual(
            date_utils.date_to_str(datetime(2020, 2, 1, 12, 10, 20)),
            '01/02/2020'
        )
