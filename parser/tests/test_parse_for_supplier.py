"""Unittests for the `parse_for_supplier` module."""

import unittest
from unittest.mock import patch
import os
from datetime import date
from .. import parse_for_supplier


TEST_INVOICES_DIR = os.path.join(
    "parser",
    "tests",
    "invoices",
)


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

    def test_invalid_supplier(self):
        """Test the class raises a `ValueError` where the supplier is not
        supplied.
        """
        with self.assertRaises(ValueError):
            DummySupplier(False, "parser/tests/test_pdf.pdf", "Invalid")

    def test_metadata(self):
        """Test that the `_metadata` method returns a default dictionary when
        not overridden.
        """
        self.assertEqual(
            parse_for_supplier.BaseSupplierParser._metadata(None),
            {},
        )


class TestSoakRochford(unittest.TestCase):
    """Tests for the `SoakRochford` class."""

    @staticmethod
    def parser_instance(filepath: str) -> parse_for_supplier.SoakRochford:
        """Return a parser instance for the given filepath and supplier.

        :param filepath: The filepath of the invoice
        :type filename: str
        :param supplier: The supplier of the invoice
        :type supplier: str
        :return: The parser instance
        :rtype: SoakRochford
        """
        return parse_for_supplier.SoakRochford(
            os.path.join(TEST_INVOICES_DIR, "soak_rochford", filepath),
            "Soak Rochford",
        )

    def setUp(self):
        """Set up the unittest."""
        self.parser = self.parser_instance("std_invoice.pdf")

    def test_items_breakdown(self):
        """Test the `_items_breakdown` method."""
        items_breakdown = self.parser._items_breakdown()
        self.assertEqual(len(items_breakdown.keys()), 28)

    @patch("parser.parse_for_supplier.ITERATION_LIMIT", 2)
    def test_items_breakdown_reaches_search_limit(self):
        """Test that the `_items_breakdown` method raises a `StopIteration`
        error when the search limit is reached.
        """
        with self.assertRaises(StopIteration):
            self.parser._items_breakdown()

    def test_order_date(self):
        """Test the `_order_date` method. It is expected to return the order
        date.
        """
        self.assertEqual(
            self.parser._order_date(),
            date(2022, 1, 2),
        )

    def test_no_order_date(self):
        """Test the `_order_date` method returns `None` when an order date
        cannot be found.
        """
        parser = self.parser_instance("no_order_date.pdf")
        self.assertIsNone(parser._order_date())


class TestTinyBoxCompany(unittest.TestCase):
    """Tests for the `TinyBoxCompany` class."""

    @staticmethod
    def parser_instance(filepath: str) -> parse_for_supplier.TinyBoxCompany:
        """Return a parser instance for the given filepath and supplier.

        :param filepath: The filepath of the invoice
        :type filename: str
        :param supplier: The supplier of the invoice
        :type supplier: str
        :return: The parser instance
        :rtype: TinyBoxCompany
        """
        return parse_for_supplier.TinyBoxCompany(
            os.path.join(TEST_INVOICES_DIR, "tiny_box_company", filepath),
            "Tiny Box Company",
        )

    def setUp(self):
        """Set up the unittest."""
        self.parser = self.parser_instance("std_invoice.pdf")

    def test_items_breakdown(self):
        """Test the `_items_breakdown` method."""
        self.assertEqual(
            self.parser._items_breakdown(),
            {
                "White FlatPack Soap Gift Box ": {
                    "price_ex_vat": "42.00",
                    "quantity": "200",
                }
            },
        )

    def test_summary(self):
        """Test the `_summary` method."""
        self.parser._summary()
        self.assertEqual(self.parser.subtotal, 42.00)
        self.assertEqual(self.parser.delivery, 4.99)
        self.assertEqual(self.parser.vat, 9.40)
        self.assertIsNone(self.parser.promotion)
        self.assertEqual(self.parser.total, 56.39)

    def test_order_number(self):
        """Test the `_order_number` method."""
        self.assertEqual(
            self.parser._order_number(),
            "123456",
        )

    def test_order_date(self):
        """Test the `_order_date` method."""
        self.assertEqual(
            self.parser._order_date(),
            date(2021, 10, 22),
        )

    def test_no_order_date(self):
        """Test that the `_order_date` method returns `None` when the order
        date cannot be found.
        """
        parser = self.parser_instance("no_order_date.pdf")
        self.assertIsNone(parser._order_date())

    def test_bad_date(self):
        """Test that the `_order_date` method returns `None` when the order
        date cannot be parsed.
        """
        parser = self.parser_instance("bad_date.pdf")
        self.assertIsNone(parser._order_date())

    def test_metadata(self):
        """Test that the `_metadata` method. It should set the value for
        the order date and order number.
        """
        self.parser._metadata()
        self.assertEqual(self.parser.order_number, "123456")
        self.assertEqual(self.parser.order_date, date(2021, 10, 22))
