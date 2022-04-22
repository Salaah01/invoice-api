"""Unittests for the `parse_for_supplier` module."""

from datetime import date
import unittest
from .. import parse_for_supplier


class DummySupplier(parse_for_supplier.BaseSupplierParser):
    """A dummy supplier parser."""

    def __init__(self, dummy_init: bool = True, *args, **kwargs):
        """Overrides the init method with the option to override certain
        functions to do nothing which in turn means that the original init
        won't perform certain actions.

        :param dummy_init: Should the original init be overridden to avoid
            processing actions? Defaults to True
        :type dummy_init: bool, optional
        """
        if dummy_init:
            self.read_invoice = lambda: []
        super().__init__(*args, **kwargs)

    def _items_breakdown(self):
        pass

    def _summary(self):
        pass

    def _metadata(self):
        pass


class TestBaseSupplierParser(unittest.TestCase):
    """Unittests for the `BaseSupplierParser` abstract class."""

    def setUp(self):
        """Set up the unittest."""
        self.parser = DummySupplier(True, "fp", "dummy supplier")

    def test_str_no_order_date(self):
        """Test that the `__str__` method returns the correct string where the
        parser object does not have an order date specified.
        """
        self.assertEqual(str(self.parser), "dummy supplier - fp")

    def test_str_with_order_date(self):
        """Test that the `__str__` method returns the correct string where the
        self.parser object does have an order date specified.
        """
        self.parser.order_date = date(2020, 1, 1)
        self.assertEqual(str(self.parser), "2020-01-01 - dummy supplier")

    def test_dict(self):
        """Test the `__dict__` method."""
        self.parser.order_number = "abc123"
        self.parser.order_date = date(2020, 1, 1)
        self.parser.subtotal = 123.45
        self.parser.vat = 23.45
        self.parser.delivery = 1.00
        self.parser.promotion = 2.00
        self.parser.total = 200

        self.assertEqual(
            self.parser.__dict__(),
            {
                "order_number": "abc123",
                "order_date": date(2020, 1, 1),
                "summary": {
                    "subtotal": 123.45,
                    "vat": 23.45,
                    "delivery": 1.00,
                    "promotion": 2.00,
                    "total": 200,
                },
                "items": None,
            },
        )

    def test_process_invoice(self):
        """Test the `process_invoice` method."""

        items = {
            "item1": {
                "name": "item1",
                "quantity": 1,
                "price": 1.00,
            }
        }

        def mock_items_breakdown():
            return items

        def mock_summary():
            self.parser.subtotal = 123.45

        def mock_metadata():
            self.parser.order_number = "abc123"

        self.parser._items_breakdown = mock_items_breakdown
        self.parser._summary = mock_summary
        self.parser._metadata = mock_metadata

        self.parser.process_invoice()

        self.assertEqual(self.parser.items_breakdown, items)
        self.assertEqual(self.parser.order_number, "abc123")
        self.assertEqual(self.parser.subtotal, 123.45)

    def test_summary(self):
        """Test the `summary` method."""
        self.parser.subtotal = 1.11
        self.parser.vat = 2.22
        self.parser.delivery = 3.33
        self.parser.promotion = 4.44
        self.parser.total = 5.55

        self.assertEqual(
            self.parser.summary(),
            {
                "subtotal": 1.11,
                "vat": 2.22,
                "delivery": 3.33,
                "promotion": 4.44,
                "total": 5.55,
            },
        )

    def test_read_invoice(self):
        """Test the `read_invoice` method."""
        parser = DummySupplier(False, "parser/tests/test_pdf.pdf", "Amazon")
        self.assertEqual(
            parser.read_invoice(),
            ["Page 1", "paragraph 1", "page 2", "paragraph 2"],
        )
