"""Unittests for the `field_choices` module."""

from django.test import SimpleTestCase
from core.field_choices import UnitChoices


class TestFieldChoices(SimpleTestCase):
    def test_unit_choices(self):
        self.assertIsInstance(UnitChoices.choices, list)
